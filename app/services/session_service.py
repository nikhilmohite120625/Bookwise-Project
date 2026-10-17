import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from app.extensions import db
from app.models.session import ReadingSession
from app.models.reading import ReadingRecord
from app.services.reading_service import ReadingService


class SessionService:

    @staticmethod
    def log_reading_session(
        user_id: int,
        duration_seconds: int,
        book_id: Optional[int] = None,
        notes: Optional[str] = None,
        pages_read: Optional[int] = None,
        started_at: Optional[datetime] = None,
        idempotency_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Logs a completed reading timer session safely with deduplication safeguard."""
        if duration_seconds <= 0:
            raise ValueError("Duration must be greater than zero seconds.")

        # Duplicate safeguard via idempotency token
        if idempotency_token:
            existing = ReadingSession.query.filter_by(
                user_id=user_id,
                idempotency_token=idempotency_token
            ).first()
            if existing:
                return {
                    'session': existing,
                    'already_recorded': True,
                    'message': 'Session was already recorded.'
                }

        token = idempotency_token or str(uuid.uuid4())
        session_start = started_at or datetime.now(timezone.utc)

        new_session = ReadingSession(
            user_id=user_id,
            book_id=book_id if (book_id and book_id > 0) else None,
            started_at=session_start,
            duration_seconds=duration_seconds,
            notes=notes,
            idempotency_token=token
        )
        db.session.add(new_session)

        # Log minutes into daily activity
        minutes = max(1, round(duration_seconds / 60))
        pages_logged = pages_read or 0

        # If book_id provided and pages_read provided, update book reading record
        if book_id and book_id > 0 and pages_read:
            record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
            if record:
                ReadingService.update_progress(user_id, book_id, record.pages_read + pages_read)
            else:
                ReadingService.set_shelf_status(
                    user_id=user_id,
                    book_id=book_id,
                    status='currently_reading',
                    pages_read=pages_read
                )
        else:
            ReadingService._increment_daily_activity(
                user_id=user_id,
                minutes_read=minutes,
                pages_read=pages_logged,
                sessions_count=1
            )

        db.session.commit()
        return {
            'session': new_session,
            'already_recorded': False,
            'message': 'Reading session recorded successfully.'
        }
