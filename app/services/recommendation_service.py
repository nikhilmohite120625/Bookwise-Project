import re
from typing import List, Dict, Any, Optional, Set
from app.models.book import Book
from app.models.preference import UserPreference
from app.models.reading import ReadingRecord
from app.models.wishlist import Wishlist


AGE_HIERARCHY = {
    'all ages': 1,
    'children': 1,
    'young adult': 2,
    'ya': 2,
    'adult': 3,
    'mature': 4
}


def normalize_token(text: str) -> str:
    """Case-fold and trim string for exact matching."""
    return text.strip().lower() if text else ""


def is_book_age_suitable(book_suitability: Optional[str], user_preference: Optional[str]) -> bool:
    """
    Evaluates age suitability:
    - User with 'All Ages' can only receive 'All Ages'
    - User with 'Young Adult' can receive 'All Ages' or 'Young Adult'
    - User with 'Adult' can receive 'All Ages', 'Young Adult', or 'Adult'
    - User with 'Mature' can receive any category
    """
    if not book_suitability or not user_preference:
        return False
    
    b_level = AGE_HIERARCHY.get(normalize_token(book_suitability), 3)
    u_level = AGE_HIERARCHY.get(normalize_token(user_preference), 3)
    
    return b_level <= u_level


class RecommendationScorer:
    """Deterministic, explainable 5-dimension recommendation engine."""

    MAX_GENRE_SCORE = 40.0
    MAX_LANGUAGE_SCORE = 20.0
    MAX_AGE_SCORE = 15.0
    MAX_DURATION_SCORE = 15.0
    MAX_INTEREST_SCORE = 10.0

    @classmethod
    def evaluate_book(cls, book: Book, preference: Optional[UserPreference]) -> Dict[str, Any]:
        """Calculates deterministic score and rationale for a single book against user preferences."""
        unconfigured_dimensions = []
        reasons = []

        # 1. Genre Compatibility (max 40)
        genre_score = 0.0
        matched_genres = []
        raw_genres = (preference.preferred_genres or []) if preference else []
        user_genres = [normalize_token(g) for g in raw_genres if g]

        if not preference or not user_genres:
            unconfigured_dimensions.append('genres')
        else:
            book_genres = [normalize_token(g) for g in book.genres_list]
            for g in book_genres:
                for ug in user_genres:
                    if g == ug or ug in g or g in ug:
                        matched_genres.append(g)
            matched_genres = sorted(list(set(matched_genres)))
            if matched_genres:
                genre_score = cls.MAX_GENRE_SCORE
                reasons.append(f"Genre Match: Aligns with your preferred genre(s) ({', '.join(g.title() for g in matched_genres)}).")
            else:
                reasons.append("Genre: Does not match any of your saved genre preferences.")

        # 2. Language Compatibility (max 20)
        lang_score = 0.0
        raw_languages = (preference.preferred_languages or []) if preference else []
        user_languages = [normalize_token(l) for l in raw_languages if l]
        book_lang = normalize_token(book.language or 'English')

        if not preference or not user_languages:
            unconfigured_dimensions.append('languages')
        else:
            if book_lang in user_languages or any(l in book_lang for l in user_languages):
                lang_score = cls.MAX_LANGUAGE_SCORE
                reasons.append(f"Language Match: Available in your preferred language ({book.language}).")
            else:
                reasons.append(f"Language: Book language ({book.language}) is not in your preferred languages list.")

        # 3. Age Suitability (max 15)
        age_score = 0.0
        user_age = preference.age_preference if preference else None

        if not preference or not user_age:
            unconfigured_dimensions.append('age_suitability')
            reasons.append("Age Suitability: Not evaluated because user age preference is unconfigured.")
        else:
            if is_book_age_suitable(book.age_suitability, user_age):
                age_score = cls.MAX_AGE_SCORE
                reasons.append(f"Age Suitability: Fully appropriate for your profile preference ({user_age}).")
            else:
                age_score = 0.0
                reasons.append(f"Age Suitability: Rated '{book.age_suitability}', which is outside your selected preference ({user_age}).")

        # 4. Reading Duration Compatibility (max 15)
        duration_score = 0.0
        target_duration = preference.preferred_duration if preference else None
        book_duration = book.estimated_duration

        if not preference or not target_duration or target_duration <= 0:
            unconfigured_dimensions.append('duration')
            reasons.append("Duration: Not evaluated because preferred duration is unconfigured.")
        elif not book_duration or book_duration <= 0:
            reasons.append("Duration: Book estimated duration is unlisted in catalogue.")
        else:
            t = float(target_duration)
            b = float(book_duration)
            diff = abs(b - t)
            ratio = max(0.0, 1.0 - (diff / t))
            duration_score = min(cls.MAX_DURATION_SCORE, max(0.0, cls.MAX_DURATION_SCORE * ratio))
            if duration_score >= 12.0:
                reasons.append(f"Duration Match: Book pace ({book_duration} mins) closely matches your target ({target_duration} mins).")
            elif duration_score > 0.0:
                reasons.append(f"Duration Partial: Book duration ({book_duration} mins) diverges moderately from your target ({target_duration} mins).")
            else:
                reasons.append(f"Duration: Book duration ({book_duration} mins) diverges substantially from target ({target_duration} mins).")

        # 5. Interest Keyword Compatibility (max 10)
        interest_score = 0.0
        raw_keywords = (preference.interest_keywords or []) if preference else []
        user_keywords = sorted(list({normalize_token(k) for k in raw_keywords if k and k.strip()}))
        matched_keywords = []
        unmatched_keywords = []

        if not preference or not user_keywords:
            unconfigured_dimensions.append('interest_keywords')
        else:
            # Build normalized searchable corpus for the book
            searchable_text = f"{book.title} {book.author} {book.description or ''} {' '.join(book.keywords_list)} {' '.join(book.genres_list)}".lower()
            
            for kw in user_keywords:
                # Exact token or phrase boundary match
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, searchable_text):
                    matched_keywords.append(kw)
                else:
                    unmatched_keywords.append(kw)

            if user_keywords:
                match_ratio = len(matched_keywords) / len(user_keywords)
                interest_score = cls.MAX_INTEREST_SCORE * match_ratio
                if matched_keywords:
                    reasons.append(f"Keyword Affinity: Matches {len(matched_keywords)} of your {len(user_keywords)} interests ({', '.join(matched_keywords)}).")
                else:
                    reasons.append("Keywords: No direct matches with your saved interest topics.")

        total_score = min(100.0, max(0.0, genre_score + lang_score + age_score + duration_score + interest_score))

        return {
            'book': book,
            'book_id': book.id,
            'total_score': total_score,
            'display_score': round(total_score, 1),
            'genre_score': round(genre_score, 2),
            'language_score': round(lang_score, 2),
            'age_score': round(age_score, 2),
            'duration_score': round(duration_score, 2),
            'interest_score': round(interest_score, 2),
            'max_scores': {
                'genre': cls.MAX_GENRE_SCORE,
                'language': cls.MAX_LANGUAGE_SCORE,
                'age': cls.MAX_AGE_SCORE,
                'duration': cls.MAX_DURATION_SCORE,
                'interest': cls.MAX_INTEREST_SCORE,
                'total': 100.0
            },
            'matched_genres': matched_genres,
            'matched_keywords': matched_keywords,
            'unmatched_keywords': unmatched_keywords,
            'unconfigured_dimensions': unconfigured_dimensions,
            'reasons': reasons
        }


def get_recommendations_for_user(
    user_id: int,
    limit: int = 20,
    include_wishlist: bool = True,
    include_reading: bool = False
) -> Dict[str, Any]:
    """
    Computes personalized recommendations for a user with strict deterministic tie-breaking.
    Tie-breaking hierarchy:
    1. Compatibility score DESC
    2. Rating DESC (None treated as 0.0)
    3. Publication year DESC (None treated as 0)
    4. Title ASC (case-insensitive)
    5. Book ID ASC
    """
    preference = UserPreference.query.filter_by(user_id=user_id).first()
    
    # Exclude books already completed
    completed_ids = {r.book_id for r in ReadingRecord.query.filter_by(user_id=user_id, status='completed').all()}
    
    # Optionally exclude currently reading
    if not include_reading:
        reading_ids = {r.book_id for r in ReadingRecord.query.filter_by(user_id=user_id, status='currently_reading').all()}
        excluded_ids = completed_ids.union(reading_ids)
    else:
        excluded_ids = completed_ids

    # Exclude wishlist if configured
    if not include_wishlist:
        wishlist_ids = {w.book_id for w in Wishlist.query.filter_by(user_id=user_id).all()}
        excluded_ids = excluded_ids.union(wishlist_ids)

    # Query all candidate books
    all_books = Book.query.all()
    candidates = [b for b in all_books if b.id not in excluded_ids]

    scored_books = [RecommendationScorer.evaluate_book(book, preference) for book in candidates]

    # Deterministic sorting
    def sort_key(item):
        b = item['book']
        return (
            -item['total_score'],
            -(b.rating if b.rating is not None else 0.0),
            -(b.publication_year if b.publication_year is not None else 0),
            (b.title or '').lower(),
            b.id
        )

    ranked = sorted(scored_books, key=sort_key)
    
    is_onboarding_needed = False
    if not preference or not preference.onboarding_completed:
        # Check if any dimension is configured
        has_any = (
            bool(preference and preference.preferred_genres) or
            bool(preference and preference.interest_keywords)
        )
        if not has_any:
            is_onboarding_needed = True

    return {
        'recommendations': ranked[:limit],
        'total_eligible': len(ranked),
        'is_onboarding_needed': is_onboarding_needed,
        'preference': preference.to_dict() if preference else None
    }
