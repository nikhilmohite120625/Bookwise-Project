from flask import Blueprint, render_template, jsonify
from app.models.book import Book
from app.models.reading import ReadingRecord
from app.forms import ALL_GENRES

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage / Landing page for BookWise Atelier."""
    # Featured books: highest rated books
    featured_books = Book.query.order_by(Book.rating.desc()).limit(6).all()
    # Recently added books
    recent_books = Book.query.order_by(Book.id.desc()).limit(6).all()
    # Total books count
    total_books = Book.query.count()

    return render_template(
        'index.html',
        featured_books=featured_books,
        recent_books=recent_books,
        total_books=total_books,
        genres=ALL_GENRES
    )


@main_bp.route('/health')
def health():
    """Health check endpoint for Render/deployment monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'BookWise Atelier',
        'version': '1.0.0'
    }), 200
