from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models.book import Book
from app.services.recommendation_service import get_recommendations_for_user, RecommendationScorer
from app.services.reading_service import ReadingService
from app.services.session_service import SessionService
from app.services.discovery_service import get_surprise_me_book, find_books_by_reading_time
from app.services.assistant_service import AssistantService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/recommendations')
@login_required
def get_recommendations():
    """REST endpoint for personalized explainable recommendations."""
    limit = request.args.get('limit', 12, type=int)
    recs = get_recommendations_for_user(user_id=current_user.id, limit=limit)
    return jsonify({
        'status': 'success',
        'is_onboarding_needed': recs['is_onboarding_needed'],
        'total_eligible': recs['total_eligible'],
        'recommendations': [
            {
                'book': r['book'].to_dict(),
                'total_score': r['total_score'],
                'display_score': r['display_score'],
                'scores': {
                    'genre': r['genre_score'],
                    'language': r['language_score'],
                    'age': r['age_score'],
                    'duration': r['duration_score'],
                    'interest': r['interest_score']
                },
                'matched_genres': r['matched_genres'],
                'matched_keywords': r['matched_keywords'],
                'reasons': r['reasons']
            }
            for r in recs['recommendations']
        ]
    })


@api_bp.route('/shelves/update', methods=['POST'])
@login_required
def update_shelf():
    """Asynchronous shelf update."""
    data = request.get_json() or {}
    book_id = data.get('book_id')
    status = data.get('status')
    pages_read = data.get('pages_read')

    if not book_id or not status:
        return jsonify({'status': 'error', 'message': 'Missing book_id or status'}), 400

    try:
        record = ReadingService.set_shelf_status(
            user_id=current_user.id,
            book_id=book_id,
            status=status,
            pages_read=pages_read
        )
        return jsonify({
            'status': 'success',
            'record': record.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api_bp.route('/timer/session', methods=['POST'])
@login_required
def log_session():
    """Asynchronous timer session logging."""
    data = request.get_json() or {}
    duration = data.get('duration_seconds')
    book_id = data.get('book_id')
    token = data.get('idempotency_token')
    notes = data.get('notes')
    pages_read = data.get('pages_read')

    if not duration or duration <= 0:
        return jsonify({'status': 'error', 'message': 'Invalid duration'}), 400

    try:
        res = SessionService.log_reading_session(
            user_id=current_user.id,
            duration_seconds=duration,
            book_id=book_id,
            notes=notes,
            pages_read=pages_read,
            idempotency_token=token
        )
        return jsonify({
            'status': 'success',
            'already_recorded': res['already_recorded'],
            'session': res['session'].to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api_bp.route('/search')
def live_search():
    """Typeahead search for books."""
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({'results': []})

    pattern = f"%{q}%"
    books = Book.query.filter(
        Book.title.ilike(pattern) | Book.author.ilike(pattern)
    ).limit(8).all()

    return jsonify({
        'results': [
            {
                'id': b.id,
                'title': b.title,
                'author': b.author,
                'rating': b.rating,
                'cover_url': b.cover_url or b.get_fallback_svg()
            }
            for b in books
        ]
    })


@api_bp.route('/surprise-me')
def surprise_me():
    """Returns a surprise book JSON."""
    user_id = current_user.id if current_user.is_authenticated else None
    book = get_surprise_me_book(user_id=user_id)
    if not book:
        return jsonify({'status': 'error', 'message': 'No books available'}), 404
    return jsonify({
        'status': 'success',
        'book': book.to_dict()
    })
