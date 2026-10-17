from datetime import datetime, timezone
from app.extensions import db


class ReadingSession(db.Model):
    __tablename__ = 'reading_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='SET NULL'), nullable=True, index=True)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    duration_seconds = db.Column(db.Integer, default=0, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    idempotency_token = db.Column(db.String(128), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='reading_sessions')
    book = db.relationship('Book', back_populates='reading_sessions')

    @property
    def duration_minutes(self) -> int:
        return max(1, round(self.duration_seconds / 60))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'started_at': self.started_at.isoformat(),
            'duration_seconds': self.duration_seconds,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<ReadingSession user={self.user_id} duration={self.duration_seconds}s>'
