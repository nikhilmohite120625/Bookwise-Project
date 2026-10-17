from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from app.models.book import Book
from app.services.discovery_service import (
    get_mood_recommendations,
    find_books_by_reading_time,
    get_surprise_me_book,
    MOOD_MAPPINGS
)

discover_bp = Blueprint('discover', __name__)


@discover_bp.route('/discover')
def index():
    """Discover Hub: Moods, reading-time finder, hidden gems, and curated highlights."""
    selected_mood = request.args.get('mood', 'comforting').lower()
    selected_time = request.args.get('time', type=int)

    # Mood-based results
    mood_data = get_mood_recommendations(selected_mood, limit=6)

    # Time-based results if requested
    time_data = None
    if selected_time:
        time_data = find_books_by_reading_time(selected_time, limit=6)

    # Hidden gems: High rated (>= 4.6), manageable length (<= 350 pages)
    hidden_gems = Book.query.filter(
        Book.rating >= 4.6,
        Book.page_count <= 350
    ).order_by(Book.rating.desc()).limit(6).all()

    return render_template(
        'discover/index.html',
        all_moods=MOOD_MAPPINGS,
        current_mood=selected_mood,
        mood_data=mood_data,
        selected_time=selected_time,
        time_data=time_data,
        hidden_gems=hidden_gems
    )


@discover_bp.route('/discover/surprise-me')
def surprise_me():
    """Surprise Me action: redirects directly to an eligible unread book."""
    user_id = current_user.id if current_user.is_authenticated else None
    book = get_surprise_me_book(user_id=user_id)
    if book:
        return redirect(url_for('books.detail', book_id=book.id))
    return redirect(url_for('books.catalogue'))
