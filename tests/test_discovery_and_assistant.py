import pytest
from app.models.book import Book
from app.services.discovery_service import (
    get_mood_recommendations,
    find_books_by_reading_time,
    get_surprise_me_book,
    get_similar_books,
    compare_books
)
from app.services.assistant_service import AssistantService


def test_mood_discovery(db):
    b1 = Book(title="Dark Forest Crime", author="A", genres=["Mystery", "Thriller"], language="English", keywords=["detective", "murder", "clue"])
    b2 = Book(title="Cozy Hearth", author="B", genres=["Fiction", "Romance"], language="English", keywords=["warmth", "cozy", "family"])
    db.session.add_all([b1, b2])
    db.session.commit()

    mysterious = get_mood_recommendations("mysterious")
    assert len(mysterious['results']) > 0
    assert mysterious['results'][0]['book'].title == "Dark Forest Crime"

    comforting = get_mood_recommendations("comforting")
    assert len(comforting['results']) > 0
    assert comforting['results'][0]['book'].title == "Cozy Hearth"


def test_reading_time_finder(db):
    b1 = Book(title="Short Story", author="A", genres=["Fiction"], language="English", estimated_duration=15)
    b2 = Book(title="Epic Chronicle", author="B", genres=["Fiction"], language="English", estimated_duration=60)
    db.session.add_all([b1, b2])
    db.session.commit()

    fast_books = find_books_by_reading_time(15)
    assert fast_books[0]['book'].title == "Short Story"


def test_assistant_query_handling(db, test_user):
    b = Book(title="The Great Detective", author="Arthur", genres=["Mystery"], language="English", estimated_duration=30, keywords=["detective", "clue"])
    db.session.add(b)
    db.session.commit()

    # Time-based query
    res_time = AssistantService.process_query(test_user.id, "I have 30 minutes to read")
    assert "Curated for a 30-minute session" in res_time['reply']
    assert len(res_time['books']) > 0

    # Mood-based query
    res_mood = AssistantService.process_query(test_user.id, "Suggest something mysterious")
    assert "Selection" in res_mood['reply']

    # Goal query
    res_goal = AssistantService.process_query(test_user.id, "How is my reading goal doing?")
    assert "Reading Progress" in res_goal['reply']
