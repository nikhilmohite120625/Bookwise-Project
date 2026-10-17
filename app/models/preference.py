from datetime import datetime, timezone
from app.extensions import db


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    preferred_genres = db.Column(db.JSON, default=list, nullable=False)
    preferred_languages = db.Column(db.JSON, default=lambda: ["English"], nullable=False)
    age_preference = db.Column(db.String(32), default='Adult', nullable=True)  # All Ages, Young Adult, Adult, Mature
    preferred_duration = db.Column(db.Integer, default=30, nullable=True)  # in minutes (session/book target)
    interest_keywords = db.Column(db.JSON, default=list, nullable=False)
    excluded_genres = db.Column(db.JSON, default=list, nullable=False)
    onboarding_completed = db.Column(db.Boolean, default=False, nullable=False)
    theme_preference = db.Column(db.String(16), default='light', nullable=False)  # 'light' or 'dark'
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', back_populates='preference')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'preferred_genres': self.preferred_genres or [],
            'preferred_languages': self.preferred_languages or [],
            'age_preference': self.age_preference,
            'preferred_duration': self.preferred_duration,
            'interest_keywords': self.interest_keywords or [],
            'excluded_genres': self.excluded_genres or [],
            'onboarding_completed': self.onboarding_completed,
            'theme_preference': self.theme_preference
        }

    def __repr__(self):
        return f'<UserPreference user_id={self.user_id} onboarding={self.onboarding_completed}>'
