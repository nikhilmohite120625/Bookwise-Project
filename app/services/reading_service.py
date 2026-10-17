from datetime import datetime, timezone, date
from typing import Optional, Dict, Any, List
from app.extensions import db
from app.models.reading import ReadingRecord
from app.models.book import Book
from app.models.activity import ReadingActivity


class ReadingService:

    @staticmethod
    def get_user_shelf(user_id: int, status: str) -> List[ReadingRecord]:
        """Fetches all records on a specific shelf for a user."""
        query = ReadingRecord.query.filter_by(user_id=user_id, status=status)
        if status == 'want_to_read':
            return query.order_by(ReadingRecord.queue_priority.asc(), ReadingRecord.updated_at.desc()).all()
        elif status == 'currently_reading':
            return query.order_by(ReadingRecord.updated_at.desc()).all()
        else:
            return query.order_by(ReadingRecord.completed_at.desc(), ReadingRecord.updated_at.desc()).all()

    @staticmethod
    def set_shelf_status(
        user_id: int,
        book_id: int,
        status: str,
        pages_read: Optional[int] = None,
        total_pages: Optional[int] = None,
        personal_rating: Optional[float] = None,
        notes: Optional[str] = None,
        completed_at: Optional[datetime] = None
    ) -> ReadingRecord:
        """Adds or moves a book to a shelf, managing dates, progress, and activity."""
        valid_statuses = {'want_to_read', 'currently_reading', 'completed'}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: '{status}'. Must be one of {valid_statuses}")

        book = Book.query.get_or_404(book_id)
        record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first()

        now = datetime.now(timezone.utc)
        resolved_total = total_pages or (record.total_pages if record else None) or book.page_count

        if not record:
            record = ReadingRecord(
                user_id=user_id,
                book_id=book_id,
                status=status,
                total_pages=resolved_total,
                pages_read=0
            )
            db.session.add(record)

        previous_status = record.status
        record.status = status
        if resolved_total:
            record.total_pages = resolved_total

        # Handle status transitions
        if status == 'currently_reading':
            if not record.started_at:
                record.started_at = now
            record.completed_at = None
            if pages_read is not None:
                record.pages_read = max(0, pages_read)
        elif status == 'completed':
            if not record.started_at:
                record.started_at = record.started_at or now
            record.completed_at = completed_at or now
            if record.total_pages and record.total_pages > 0:
                record.pages_read = record.total_pages
            elif pages_read is not None:
                record.pages_read = max(0, pages_read)
            
            # Record daily activity increment if moving to completed
            if previous_status != 'completed':
                ReadingService._increment_daily_activity(user_id, books_completed=1)
        elif status == 'want_to_read':
            record.completed_at = None
            if pages_read is not None:
                record.pages_read = max(0, pages_read)

        # Validate pages
        if record.total_pages and record.pages_read > record.total_pages:
            record.pages_read = record.total_pages
        if record.pages_read < 0:
            record.pages_read = 0

        if personal_rating is not None:
            record.personal_rating = max(1.0, min(5.0, float(personal_rating)))
        if notes is not None:
            record.notes = notes

        record.updated_at = now
        db.session.commit()
        return record

    @staticmethod
    def update_progress(
        user_id: int,
        book_id: int,
        pages_read: int,
        notes: Optional[str] = None
    ) -> ReadingRecord:
        """Updates reading progress for currently reading or shelf books."""
        record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first_or_404()
        
        old_pages = record.pages_read
        total = record.total_pages or (record.book.page_count if record.book else 100)
        
        clamped_pages = max(0, min(total, pages_read))
        pages_diff = max(0, clamped_pages - old_pages)
        
        record.pages_read = clamped_pages
        if notes is not None:
            record.notes = notes

        # If read completely, mark completed
        now = datetime.now(timezone.utc)
        if record.pages_read >= total and record.status != 'completed':
            record.status = 'completed'
            record.completed_at = now
            ReadingService._increment_daily_activity(user_id, books_completed=1, pages_read=pages_diff)
        else:
            if pages_diff > 0:
                ReadingService._increment_daily_activity(user_id, pages_read=pages_diff)

        record.updated_at = now
        db.session.commit()
        return record

    @staticmethod
    def remove_from_shelf(user_id: int, book_id: int) -> bool:
        """Removes a reading record safely."""
        record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False

    @staticmethod
    def reorder_queue(user_id: int, ordered_book_ids: List[int]):
        """Persists custom queue priority order for Want to Read shelf."""
        for position, book_id in enumerate(ordered_book_ids):
            record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
            if record:
                record.queue_priority = position
        db.session.commit()

    @staticmethod
    def _increment_daily_activity(
        user_id: int,
        minutes_read: int = 0,
        pages_read: int = 0,
        books_completed: int = 0,
        sessions_count: int = 0
    ):
        """Authoritatively logs daily activity for streak and calendar tracking."""
        today = date.today()
        activity = ReadingActivity.query.filter_by(user_id=user_id, activity_date=today).first()
        if not activity:
            activity = ReadingActivity(
                user_id=user_id,
                activity_date=today,
                minutes_read=minutes_read,
                pages_read=pages_read,
                books_completed=books_completed,
                sessions_count=sessions_count
            )
            db.session.add(activity)
        else:
            activity.minutes_read += minutes_read
            activity.pages_read += pages_read
            activity.books_completed += books_completed
            activity.sessions_count += sessions_count
            activity.updated_at = datetime.now(timezone.utc)
        db.session.flush()
