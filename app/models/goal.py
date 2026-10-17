from datetime import datetime, timezone
from app.extensions import db


class ReadingGoal(db.Model):
    __tablename__ = 'reading_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    target_books = db.Column(db.Integer, default=12, nullable=False)
    goal_year = db.Column(db.Integer, default=lambda: datetime.now(timezone.utc).year, nullable=False, index=True)
    monthly_target = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('user_id', 'goal_year', name='uq_user_goal_year'),
    )

    user = db.relationship('User', back_populates='reading_goals')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_books': self.target_books,
            'goal_year': self.goal_year,
            'monthly_target': self.monthly_target
        }

    def __repr__(self):
        return f'<ReadingGoal user={self.user_id} year={self.goal_year} target={self.target_books}>'
