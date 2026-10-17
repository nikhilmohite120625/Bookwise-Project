from datetime import datetime, timezone
from app.extensions import db


class ReadingRecord(db.Model):
    __tablename__ = 'reading_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(32), default='want_to_read', nullable=False)  # 'want_to_read', 'currently_reading', 'completed'
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    pages_read = db.Column(db.Integer, default=0, nullable=False)
    total_pages = db.Column(db.Integer, nullable=True)
    personal_rating = db.Column(db.Float, nullable=True)  # 1.0 to 5.0
    notes = db.Column(db.Text, nullable=True)
    queue_priority = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book_reading'),
    )

    user = db.relationship('User', back_populates='reading_records')
    book = db.relationship('Book', back_populates='reading_records')

    @property
    def progress_percent(self) -> int:
        pages = self.total_pages or (self.book.page_count if self.book else None)
        if not pages or pages <= 0:
            return 100 if self.status == 'completed' else 0
        read = max(0, self.pages_read or 0)
        pct = int(min(100, (read / pages) * 100))
        if self.status == 'completed':
            return 100
        return pct

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'pages_read': self.pages_read,
            'total_pages': self.total_pages or (self.book.page_count if self.book else None),
            'progress_percent': self.progress_percent,
            'personal_rating': self.personal_rating,
            'notes': self.notes,
            'queue_priority': self.queue_priority,
            'book': self.book.to_dict() if self.book else None
        }

    def __repr__(self):
        return f'<ReadingRecord user={self.user_id} book={self.book_id} status={self.status}>'
