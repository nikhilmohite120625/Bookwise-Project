from datetime import datetime, timezone
from typing import List, Optional
from app.extensions import db
from app.models.journal import ReadingJournalEntry


class JournalService:

    @staticmethod
    def get_user_entries(user_id: int, book_id: Optional[int] = None) -> List[ReadingJournalEntry]:
        """Gets private reading journal entries for a user, optionally filtered by book."""
        query = ReadingJournalEntry.query.filter_by(user_id=user_id)
        if book_id:
            query = query.filter_by(book_id=book_id)
        return query.order_by(ReadingJournalEntry.created_at.desc()).all()

    @staticmethod
    def create_entry(
        user_id: int,
        title: str,
        content: str,
        book_id: Optional[int] = None,
        reading_record_id: Optional[int] = None
    ) -> ReadingJournalEntry:
        """Creates a private journal reflection."""
        entry = ReadingJournalEntry(
            user_id=user_id,
            title=title.strip(),
            content=content.strip(),
            book_id=book_id if (book_id and book_id > 0) else None,
            reading_record_id=reading_record_id if (reading_record_id and reading_record_id > 0) else None
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def update_entry(entry_id: int, user_id: int, title: str, content: str) -> Optional[ReadingJournalEntry]:
        """Updates a private journal entry with ownership verification."""
        entry = ReadingJournalEntry.query.filter_by(id=entry_id, user_id=user_id).first_or_404()
        entry.title = title.strip()
        entry.content = content.strip()
        entry.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return entry

    @staticmethod
    def delete_entry(entry_id: int, user_id: int) -> bool:
        """Deletes a journal entry safely with ownership verification."""
        entry = ReadingJournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return True
        return False
