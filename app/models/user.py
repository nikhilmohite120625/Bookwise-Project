from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(191), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships with cascade delete
    preference = db.relationship('UserPreference', back_populates='user', uselist=False, cascade='all, delete-orphan')
    reading_records = db.relationship('ReadingRecord', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    wishlist_items = db.relationship('Wishlist', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    reading_goals = db.relationship('ReadingGoal', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    reading_sessions = db.relationship('ReadingSession', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    journal_entries = db.relationship('ReadingJournalEntry', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    collections = db.relationship('PersonalCollection', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    reading_activities = db.relationship('ReadingActivity', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
