from datetime import datetime, timezone
from app.extensions import db


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book_wishlist'),
    )

    user = db.relationship('User', back_populates='wishlist_items')
    book = db.relationship('Book', back_populates='wishlist_items')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'added_at': self.added_at.isoformat(),
            'book': self.book.to_dict() if self.book else None
        }

    def __repr__(self):
        return f'<Wishlist user={self.user_id} book={self.book_id}>'
