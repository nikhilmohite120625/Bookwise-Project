from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import or_
from app.models.book import Book
from app.models.reading import ReadingRecord
from app.models.wishlist import Wishlist
from app.services.recommendation_service import RecommendationScorer
from app.services.discovery_service import get_similar_books, compare_books
from app.forms import ALL_GENRES, ALL_LANGUAGES, AGE_CATEGORIES

books_bp = Blueprint('books', __name__)


@books_bp.route('/catalogue')
def catalogue():
    """Public catalogue with multi-facet filtering, search, sorting, and pagination."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    selected_genre = request.args.get('genre', '').strip()
    selected_language = request.args.get('language', '').strip()
    selected_age = request.args.get('age', '').strip()
    min_rating = request.args.get('rating', type=float)
    max_duration = request.args.get('duration', type=int)
    sort_by = request.args.get('sort', 'rating_desc').strip()

    query = Book.query

    # Search filter
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_pattern),
                Book.author.ilike(search_pattern),
                Book.description.ilike(search_pattern)
            )
        )

    # Genre filter (searches JSON array)
    if selected_genre:
        query = query.filter(Book.genres.contains(selected_genre))

    # Language filter
    if selected_language:
        query = query.filter(Book.language == selected_language)

    # Age suitability filter
    if selected_age:
        query = query.filter(Book.age_suitability == selected_age)

    # Minimum rating filter
    if min_rating:
        query = query.filter(Book.rating >= min_rating)

    # Maximum duration filter
    if max_duration:
        query = query.filter(Book.estimated_duration <= max_duration)

    # Sorting
    if sort_by == 'title_asc':
        query = query.order_by(Book.title.asc())
    elif sort_by == 'year_desc':
        query = query.order_by(Book.publication_year.desc().nullslast())
    elif sort_by == 'duration_asc':
        query = query.order_by(Book.estimated_duration.asc().nullslast())
    else:  # default rating_desc
        query = query.order_by(Book.rating.desc().nullslast(), Book.title.asc())

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    books = pagination.items

    # Fetch user reading shelf records if logged in for badge states
    user_records = {}
    user_wishlist_ids = set()
    if current_user.is_authenticated:
        records = ReadingRecord.query.filter_by(user_id=current_user.id).all()
        user_records = {r.book_id: r.status for r in records}
        wishlists = Wishlist.query.filter_by(user_id=current_user.id).all()
        user_wishlist_ids = {w.book_id for w in wishlists}

    return render_template(
        'books/index.html',
        books=books,
        pagination=pagination,
        search_query=search_query,
        selected_genre=selected_genre,
        selected_language=selected_language,
        selected_age=selected_age,
        min_rating=min_rating,
        max_duration=max_duration,
        sort_by=sort_by,
        all_genres=ALL_GENRES,
        all_languages=ALL_LANGUAGES,
        age_categories=AGE_CATEGORIES,
        user_records=user_records,
        user_wishlist_ids=user_wishlist_ids
    )


@books_bp.route('/books/<int:book_id>')
def detail(book_id: int):
    """Detailed book view with similar books and personalized explainable compatibility score."""
    book = Book.query.get_or_404(book_id)
    similar = get_similar_books(book.id, limit=4)

    eval_data = None
    user_record = None
    in_wishlist = False

    if current_user.is_authenticated:
        eval_data = RecommendationScorer.evaluate_book(book, current_user.preference)
        user_record = ReadingRecord.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, book_id=book.id).first() is not None

    return render_template(
        'books/detail.html',
        book=book,
        similar_books=similar,
        eval_data=eval_data,
        user_record=user_record,
        in_wishlist=in_wishlist
    )


@books_bp.route('/compare')
def compare():
    """Compare 2 or 3 books side-by-side."""
    book_ids_param = request.args.getlist('id', type=int)
    # Also support comma-separated b=1,2
    if not book_ids_param and request.args.get('b'):
        try:
            book_ids_param = [int(x) for x in request.args.get('b').split(',') if x.strip().isdigit()]
        except ValueError:
            book_ids_param = []

    # Limit to max 3 books
    book_ids = book_ids_param[:3]
    if len(book_ids) < 2:
        # Default to top 2 books if not enough specified
        default_books = Book.query.order_by(Book.rating.desc()).limit(2).all()
        book_ids = [b.id for b in default_books]

    comparison_data = compare_books(
        book_ids=book_ids,
        user_id=current_user.id if current_user.is_authenticated else None
    )

    all_books_options = Book.query.order_by(Book.title.asc()).all()

    return render_template(
        'books/compare.html',
        comparison_data=comparison_data,
        all_books=all_books_options,
        selected_ids=book_ids
    )
