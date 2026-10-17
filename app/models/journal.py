from datetime import datetime, timezone
from app.extensions import db


class ReadingJournalEntry(db.Model):
    __tablename__ = 'reading_journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='SET NULL'), nullable=True, index=True)
    reading_record_id = db.Column(db.Integer, db.ForeignKey('reading_records.id', ondelete='SET NULL'), nullable=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', back_populates='journal_entries')
    book = db.relationship('Book', back_populates='journal_entries')
    reading_record = db.relationship('ReadingRecord')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'reading_record_id': self.reading_record_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<ReadingJournalEntry user={self.user_id} title="{self.title[:20]}">'
