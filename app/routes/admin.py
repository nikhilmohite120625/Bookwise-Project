from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.book import Book
from app.models.user import User
from app.models.reading import ReadingRecord
from app.forms import BookAdminForm
from seeds.sample_books import seed_database

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator ensuring current user is an authenticated administrator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin:
            flash('Access denied. Administrator privileges required.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard overview."""
    total_books = Book.query.count()
    total_users = User.query.count()
    total_records = ReadingRecord.query.count()
    recent_books = Book.query.order_by(Book.id.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        total_books=total_books,
        total_users=total_users,
        total_records=total_records,
        recent_books=recent_books
    )


@admin_bp.route('/books')
@admin_required
def books_list():
    """List of all books for management with pagination and search."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '').strip()

    query = Book.query
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%"))

    pagination = query.order_by(Book.id.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/books_list.html', books=pagination.items, pagination=pagination, search=search)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add a new book to the catalogue."""
    form = BookAdminForm()
    if form.validate_on_submit():
        if isinstance(form.genres.data, list):
            genres_list = form.genres.data
        else:
            genres_list = [g.strip() for g in (form.genres.data or '').split(',') if g.strip()]

        if isinstance(form.keywords.data, list):
            keywords_list = [k.strip().lower() for k in form.keywords.data if k and k.strip()]
        else:
            keywords_list = [k.strip().lower() for k in (form.keywords.data or '').split(',') if k.strip()]

        book = Book(
            title=form.title.data.strip(),
            author=form.author.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            genres=genres_list,
            language=form.language.data.strip(),
            publication_year=form.publication_year.data,
            age_suitability=form.age_suitability.data,
            estimated_duration=form.estimated_duration.data,
            keywords=keywords_list,
            rating=form.rating.data or 4.5,
            isbn=form.isbn.data.strip() if form.isbn.data else None,
            cover_url=form.cover_url.data.strip() if form.cover_url.data else None,
            page_count=form.page_count.data
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{book.title}" added to catalogue successfully.', 'success')
        return redirect(url_for('admin.books_list'))

    return render_template('admin/book_form.html', form=form, title='Add New Book')


@admin_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id: int):
    """Edit an existing book in the catalogue."""
    book = Book.query.get_or_404(book_id)
    form = BookAdminForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data.strip()
        book.author = form.author.data.strip()
        book.description = form.description.data.strip() if form.description.data else None
        if isinstance(form.genres.data, list):
            book.genres = form.genres.data
        else:
            book.genres = [g.strip() for g in (form.genres.data or '').split(',') if g.strip()]

        book.language = form.language.data.strip()
        book.publication_year = form.publication_year.data
        book.age_suitability = form.age_suitability.data
        book.estimated_duration = form.estimated_duration.data

        if isinstance(form.keywords.data, list):
            book.keywords = [k.strip().lower() for k in form.keywords.data if k and k.strip()]
        else:
            book.keywords = [k.strip().lower() for k in (form.keywords.data or '').split(',') if k.strip()]
        book.rating = form.rating.data
        book.isbn = form.isbn.data.strip() if form.isbn.data else None
        book.cover_url = form.cover_url.data.strip() if form.cover_url.data else None
        book.page_count = form.page_count.data

        db.session.commit()
        flash(f'Book "{book.title}" updated successfully.', 'success')
        return redirect(url_for('admin.books_list'))

    if request.method == 'GET':
        form.genres.data = ', '.join(book.genres_list)
        form.keywords.data = ', '.join(book.keywords_list)

    return render_template('admin/book_form.html', form=form, book=book, title=f'Edit "{book.title}"')


@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@admin_required
def delete_book(book_id: int):
    """Delete a book from the catalogue."""
    book = Book.query.get_or_404(book_id)
    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f'Book "{title}" has been deleted from the catalogue.', 'info')
    return redirect(url_for('admin.books_list'))


@admin_bp.route('/seed-catalogue', methods=['POST'])
@admin_required
def seed_catalogue():
    """Bulk imports sample books into catalogue."""
    added = seed_database(db)
    flash(f'Catalogue seeded successfully! Added {added} books.', 'success')
    return redirect(url_for('admin.dashboard'))
