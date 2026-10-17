import pytest
from app.models.book import Book
from app.models.reading import ReadingRecord
from app.models.activity import ReadingActivity
from app.services.reading_service import ReadingService


def test_shelf_transitions_and_uniqueness(db, test_user):
    book = Book(title="Shelf Master", author="Author", genres=["Fiction"], language="English", page_count=300)
    db.session.add(book)
    db.session.commit()

    # Add to Want to Read
    rec1 = ReadingService.set_shelf_status(user_id=test_user.id, book_id=book.id, status='want_to_read')
    assert rec1.status == 'want_to_read'
    assert ReadingRecord.query.filter_by(user_id=test_user.id, book_id=book.id).count() == 1

    # Move to Currently Reading
    rec2 = ReadingService.set_shelf_status(user_id=test_user.id, book_id=book.id, status='currently_reading', pages_read=50)
    assert rec2.id == rec1.id
    assert rec2.status == 'currently_reading'
    assert rec2.started_at is not None
    assert rec2.pages_read == 50
    assert ReadingRecord.query.filter_by(user_id=test_user.id, book_id=book.id).count() == 1

    # Move to Completed
    rec3 = ReadingService.set_shelf_status(user_id=test_user.id, book_id=book.id, status='completed')
    assert rec3.id == rec1.id
    assert rec3.status == 'completed'
    assert rec3.completed_at is not None
    assert rec3.pages_read == 300  # Automatically sets to total_pages
    assert ReadingRecord.query.filter_by(user_id=test_user.id, book_id=book.id).count() == 1


def test_page_bounds_validation(db, test_user):
    book = Book(title="Bounds Test", author="Author", genres=["Fiction"], language="English", page_count=200)
    db.session.add(book)
    db.session.commit()

    ReadingService.set_shelf_status(user_id=test_user.id, book_id=book.id, status='currently_reading', total_pages=200)
    
    # Progress exceeds total pages -> clamped to total
    rec = ReadingService.update_progress(user_id=test_user.id, book_id=book.id, pages_read=250)
    assert rec.pages_read == 200
    assert rec.status == 'completed'  # auto marked completed when reaching total


def test_remove_from_shelf(db, test_user):
    book = Book(title="To Remove", author="Author", genres=["Fiction"], language="English")
    db.session.add(book)
    db.session.commit()

    ReadingService.set_shelf_status(user_id=test_user.id, book_id=book.id, status='want_to_read')
    assert ReadingRecord.query.filter_by(user_id=test_user.id, book_id=book.id).first() is not None

    removed = ReadingService.remove_from_shelf(user_id=test_user.id, book_id=book.id)
    assert removed is True
    assert ReadingRecord.query.filter_by(user_id=test_user.id, book_id=book.id).first() is None
