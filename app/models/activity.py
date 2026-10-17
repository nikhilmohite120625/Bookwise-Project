from datetime import datetime, date, timezone
from app.extensions import db


class ReadingActivity(db.Model):
    __tablename__ = 'reading_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    activity_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    minutes_read = db.Column(db.Integer, default=0, nullable=False)
    pages_read = db.Column(db.Integer, default=0, nullable=False)
    books_completed = db.Column(db.Integer, default=0, nullable=False)
    sessions_count = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('user_id', 'activity_date', name='uq_user_activity_date'),
    )

    user = db.relationship('User', back_populates='reading_activities')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_date': self.activity_date.isoformat(),
            'minutes_read': self.minutes_read,
            'pages_read': self.pages_read,
            'books_completed': self.books_completed,
            'sessions_count': self.sessions_count
        }

    def __repr__(self):
        return f'<ReadingActivity user={self.user_id} date={self.activity_date} mins={self.minutes_read}>'
