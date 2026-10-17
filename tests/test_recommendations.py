import pytest
from app.models.book import Book
from app.models.preference import UserPreference
from app.models.reading import ReadingRecord
from app.services.recommendation_service import (
    RecommendationScorer,
    get_recommendations_for_user,
    is_book_age_suitable
)


def test_genre_scoring():
    book = Book(
        title="Fantasy Quest",
        author="Author A",
        genres=["Fantasy", "Adventure"],
        language="English",
        age_suitability="Adult",
        estimated_duration=30,
        keywords=[]
    )
    # Match
    pref_match = UserPreference(preferred_genres=["Fantasy", "Sci-Fi"])
    res1 = RecommendationScorer.evaluate_book(book, pref_match)
    assert res1['genre_score'] == 40.0
    assert 'Fantasy' in [g.title() for g in res1['matched_genres']]

    # No match
    pref_no_match = UserPreference(preferred_genres=["Romance", "History"])
    res2 = RecommendationScorer.evaluate_book(book, pref_no_match)
    assert res2['genre_score'] == 0.0

    # Unconfigured
    pref_empty = UserPreference(preferred_genres=[])
    res3 = RecommendationScorer.evaluate_book(book, pref_empty)
    assert res3['genre_score'] == 0.0
    assert 'genres' in res3['unconfigured_dimensions']


def test_language_scoring():
    book = Book(
        title="French Volume",
        author="Author B",
        genres=["Philosophy"],
        language="French",
        age_suitability="Adult",
        estimated_duration=30,
        keywords=[]
    )
    pref_match = UserPreference(preferred_languages=["English", "French"])
    res1 = RecommendationScorer.evaluate_book(book, pref_match)
    assert res1['language_score'] == 20.0

    pref_no_match = UserPreference(preferred_languages=["English", "Spanish"])
    res2 = RecommendationScorer.evaluate_book(book, pref_no_match)
    assert res2['language_score'] == 0.0


def test_age_suitability_scoring():
    adult_book = Book(
        title="Adult Thriller",
        author="Author C",
        genres=["Thriller"],
        language="English",
        age_suitability="Adult",
        estimated_duration=30,
        keywords=[]
    )
    ya_book = Book(
        title="YA Fantasy",
        author="Author D",
        genres=["Fantasy"],
        language="English",
        age_suitability="Young Adult",
        estimated_duration=30,
        keywords=[]
    )
    # Adult user can read Adult and YA books
    pref_adult = UserPreference(age_preference="Adult")
    assert RecommendationScorer.evaluate_book(adult_book, pref_adult)['age_score'] == 15.0
    assert RecommendationScorer.evaluate_book(ya_book, pref_adult)['age_score'] == 15.0

    # Young Adult user CANNOT read Adult books
    pref_ya = UserPreference(age_preference="Young Adult")
    assert RecommendationScorer.evaluate_book(adult_book, pref_ya)['age_score'] == 0.0
    assert RecommendationScorer.evaluate_book(ya_book, pref_ya)['age_score'] == 15.0


def test_duration_scoring():
    pref = UserPreference(preferred_duration=30)

    # Perfect match: T=30, B=30 -> 15.0
    b_perfect = Book(title="Perfect", author="A", genres=[], language="", estimated_duration=30, keywords=[])
    res1 = RecommendationScorer.evaluate_book(b_perfect, pref)
    assert res1['duration_score'] == 15.0

    # Half divergence: T=30, B=45 -> |45 - 30| / 30 = 0.5 -> 15 * 0.5 = 7.5
    b_half = Book(title="Half", author="A", genres=[], language="", estimated_duration=45, keywords=[])
    res2 = RecommendationScorer.evaluate_book(b_half, pref)
    assert res2['duration_score'] == 7.5

    # Full divergence: T=30, B=75 -> |75 - 30| / 30 = 1.5 -> clamped to 0.0
    b_zero = Book(title="Zero", author="A", genres=[], language="", estimated_duration=75, keywords=[])
    res3 = RecommendationScorer.evaluate_book(b_zero, pref)
    assert res3['duration_score'] == 0.0


def test_keyword_scoring():
    book = Book(
        title="The Empire of Stars",
        author="Galaxy Author",
        description="A sweeping quest across the cosmos discovering alien mysteries and deep space adventures.",
        genres=["Science Fiction"],
        language="English",
        keywords=["space", "alien", "galaxy"]
    )

    # 2 out of 3 matched: 'space', 'quest' in text, 'stoicism' not
    pref = UserPreference(interest_keywords=["space", "quest", "stoicism"])
    res = RecommendationScorer.evaluate_book(book, pref)
    # 10 * (2/3) = 6.67
    assert pytest.approx(res['interest_score'], 0.01) == 6.67
    assert "space" in res['matched_keywords']
    assert "quest" in res['matched_keywords']
    assert "stoicism" in res['unmatched_keywords']


def test_recommendations_ranking_and_eligibility(db, test_user):
    b1 = Book(title="Alpha Book", author="Author 1", genres=["Fantasy"], language="English", age_suitability="Adult", estimated_duration=30, rating=4.8, publication_year=2020, keywords=["magic"])
    b2 = Book(title="Beta Book", author="Author 2", genres=["Philosophy"], language="English", age_suitability="Adult", estimated_duration=30, rating=4.5, publication_year=2019, keywords=["stoicism"])
    b3 = Book(title="Gamma Completed", author="Author 3", genres=["Fantasy"], language="English", age_suitability="Adult", estimated_duration=30, rating=5.0, publication_year=2021, keywords=["magic"])

    db.session.add_all([b1, b2, b3])
    db.session.commit()

    # Mark b3 as completed for test_user
    rec = ReadingRecord(user_id=test_user.id, book_id=b3.id, status='completed')
    db.session.add(rec)
    db.session.commit()

    results = get_recommendations_for_user(test_user.id)
    recs = results['recommendations']

    # b3 must be excluded because it is completed
    rec_ids = [r['book'].id for r in recs]
    assert b3.id not in rec_ids
    assert b1.id in rec_ids
    assert b2.id in rec_ids
