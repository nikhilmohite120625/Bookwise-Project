import random
from typing import List, Dict, Any, Optional
from app.extensions import db
from app.models.book import Book
from app.models.reading import ReadingRecord
from app.models.preference import UserPreference
from app.services.recommendation_service import (
    RecommendationScorer,
    is_book_age_suitable,
    normalize_token
)

MOOD_MAPPINGS = {
    'comforting': {
        'genres': ['fiction', 'romance', 'young adult', 'children\'s literature', 'self-help'],
        'keywords': ['cozy', 'warmth', 'family', 'heart', 'friendship', 'nostalgia', 'peace', 'home'],
        'tagline': 'Warm, restorative reads that feel like a cup of tea by the fireplace.'
    },
    'adventurous': {
        'genres': ['fantasy', 'adventure', 'science fiction'],
        'keywords': ['journey', 'quest', 'exploration', 'magic', 'danger', 'survival', 'wild', 'expedition'],
        'tagline': 'Epic journeys, bold expeditions, and thrilling unknowns.'
    },
    'thought-provoking': {
        'genres': ['philosophy', 'history', 'biography', 'technology', 'science fiction'],
        'keywords': ['society', 'truth', 'ethics', 'future', 'mind', 'ideas', 'wisdom', 'meaning'],
        'tagline': 'Deep inquiries into human nature, society, and ideas.'
    },
    'mysterious': {
        'genres': ['mystery', 'thriller'],
        'keywords': ['detective', 'crime', 'secret', 'puzzle', 'investigation', 'murder', 'clue', 'shadow'],
        'tagline': 'Intriguing puzzles, unsolved riddles, and secrets in the shadows.'
    },
    'inspiring': {
        'genres': ['biography', 'self-help', 'philosophy', 'history'],
        'keywords': ['triumph', 'courage', 'hope', 'growth', 'resilience', 'leadership', 'purpose'],
        'tagline': 'Uplifting life stories and philosophical fuel for your ambition.'
    },
    'educational': {
        'genres': ['technology', 'history', 'education', 'philosophy'],
        'keywords': ['learning', 'science', 'innovation', 'discoveries', 'engineering', 'knowledge', 'history'],
        'tagline': 'Expand your mental model of the world and master new disciplines.'
    },
    'lighthearted': {
        'genres': ['fiction', 'young adult', 'romance'],
        'keywords': ['witty', 'fun', 'humor', 'quirky', 'charming', 'sweet', 'playful'],
        'tagline': 'Breezy, charming, and delightful reading experiences.'
    },
    'romantic': {
        'genres': ['romance', 'fiction'],
        'keywords': ['love', 'passion', 'relationship', 'heart', 'longing', 'marriage', 'destiny'],
        'tagline': 'Passionate connections, intimate bonds, and heartstrings pulled.'
    },
    'suspenseful': {
        'genres': ['thriller', 'mystery', 'science fiction'],
        'keywords': ['tension', 'paranoia', 'chase', 'twist', 'conspiracy', 'danger', 'countdown'],
        'tagline': 'Fast-paced, edge-of-your-seat tension that refuses to let you sleep.'
    }
}


def get_mood_recommendations(mood_name: str, limit: int = 12) -> Dict[str, Any]:
    """Finds books matching a given mood deterministically by genre and keyword affinity."""
    mood_key = normalize_token(mood_name)
    mood_config = MOOD_MAPPINGS.get(mood_key)
    if not mood_config:
        return {'mood': mood_name, 'books': [], 'tagline': 'Mood not recognized.'}

    target_genres = [normalize_token(g) for g in mood_config['genres']]
    target_keywords = [normalize_token(k) for k in mood_config['keywords']]

    all_books = Book.query.all()
    scored = []

    for book in all_books:
        score = 0
        matches = []

        # Check genre matches
        book_genres = [normalize_token(g) for g in book.genres_list]
        matched_g = [g for g in book_genres if any(tg in g or g in tg for tg in target_genres)]
        if matched_g:
            score += len(matched_g) * 30
            matches.append(f"Genres: {', '.join(g.title() for g in matched_g)}")

        # Check keyword matches
        searchable_text = f"{book.title} {book.description or ''} {' '.join(book.keywords_list)}".lower()
        matched_kw = [k for k in target_keywords if k in searchable_text]
        if matched_kw:
            score += len(matched_kw) * 10
            matches.append(f"Keywords: {', '.join(matched_kw[:3])}")

        if score > 0:
            scored.append({
                'book': book,
                'score': score,
                'rating': book.rating or 0.0,
                'matches': matches
            })

    # Sort by mood match score DESC, then rating DESC, then title ASC
    scored.sort(key=lambda x: (-x['score'], -x['rating'], x['book'].title.lower()))
    return {
        'mood': mood_name.capitalize(),
        'tagline': mood_config['tagline'],
        'results': scored[:limit]
    }


def find_books_by_reading_time(target_minutes: int, limit: int = 12) -> List[Dict[str, Any]]:
    """Ranks books by proximity of estimated reading duration to target minutes."""
    all_books = Book.query.all()
    results = []

    for book in all_books:
        duration = book.estimated_duration or 30
        diff = abs(duration - target_minutes)
        closeness_score = max(0, 100 - (diff * 2))
        results.append({
            'book': book,
            'duration': duration,
            'diff': diff,
            'closeness_score': closeness_score
        })

    # Sort by closeness (diff ASC), then rating DESC, then title ASC
    results.sort(key=lambda x: (x['diff'], -(x['book'].rating or 0), x['book'].title.lower()))
    return results[:limit]


def get_surprise_me_book(user_id: Optional[int] = None) -> Optional[Book]:
    """Selects an eligible catalogue book respecting user suitability and unread status."""
    query = Book.query
    preference = None

    if user_id:
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        completed_ids = {r.book_id for r in ReadingRecord.query.filter_by(user_id=user_id, status='completed').all()}
        if completed_ids:
            query = query.filter(Book.id.notin_(completed_ids))

    candidates = query.all()
    if preference and preference.age_preference:
        candidates = [b for b in candidates if is_book_age_suitable(b.age_suitability, preference.age_preference)]

    if not candidates:
        # Fallback to any book if all filtered out
        candidates = Book.query.all()

    return random.choice(candidates) if candidates else None


def get_similar_books(book_id: int, limit: int = 6) -> List[Dict[str, Any]]:
    """Calculates deterministic similarity between target book and all other catalogue books."""
    target_book = db.session.get(Book, book_id)
    if not target_book:
        return []

    target_genres = {normalize_token(g) for g in target_book.genres_list}
    target_keywords = {normalize_token(k) for k in target_book.keywords_list}
    target_author = normalize_token(target_book.author)

    other_books = Book.query.filter(Book.id != book_id).all()
    scored = []

    for candidate in other_books:
        cand_genres = {normalize_token(g) for g in candidate.genres_list}
        cand_keywords = {normalize_token(k) for k in candidate.keywords_list}
        cand_author = normalize_token(candidate.author)

        shared_genres = target_genres.intersection(cand_genres)
        shared_keywords = target_keywords.intersection(cand_keywords)
        same_author = (cand_author == target_author)

        score = (len(shared_genres) * 35) + (len(shared_keywords) * 15)
        if same_author:
            score += 40

        shared_reasons = []
        if same_author:
            shared_reasons.append(f"Written by the same author ({candidate.author})")
        if shared_genres:
            shared_reasons.append(f"Shared genre: {', '.join(g.title() for g in shared_genres)}")
        if shared_keywords:
            shared_reasons.append(f"Related themes: {', '.join(shared_keywords)}")

        if score > 0:
            scored.append({
                'book': candidate,
                'similarity_score': min(100, score),
                'shared_reasons': shared_reasons
            })

    scored.sort(key=lambda x: (-x['similarity_score'], -(x['book'].rating or 0), x['book'].title.lower()))
    return scored[:limit]


def compare_books(book_ids: List[int], user_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Generates comparison matrix for 2-3 books including user compatibility scores."""
    books = Book.query.filter(Book.id.in_(book_ids)).all()
    preference = UserPreference.query.filter_by(user_id=user_id).first() if user_id else None

    comparison_data = []
    for book in books:
        eval_data = RecommendationScorer.evaluate_book(book, preference)
        comparison_data.append({
            'book': book,
            'evaluation': eval_data
        })

    return comparison_data
