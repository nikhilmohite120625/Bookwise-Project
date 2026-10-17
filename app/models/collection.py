from datetime import datetime, timezone
from app.extensions import db


class PersonalCollection(db.Model):
    __tablename__ = 'personal_collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', back_populates='collections')
    items = db.relationship(
        'CollectionItem',
        back_populates='collection',
        cascade='all, delete-orphan',
        order_by='CollectionItem.position',
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'items_count': self.items.count(),
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<PersonalCollection user={self.user_id} name="{self.name}">'


class CollectionItem(db.Model):
    __tablename__ = 'collection_items'

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('personal_collections.id', ondelete='CASCADE'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False, index=True)
    position = db.Column(db.Integer, default=0, nullable=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('collection_id', 'book_id', name='uq_collection_book'),
    )

    collection = db.relationship('PersonalCollection', back_populates='items')
    book = db.relationship('Book', back_populates='collection_items')

    def to_dict(self):
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'book_id': self.book_id,
            'position': self.position,
            'added_at': self.added_at.isoformat(),
            'book': self.book.to_dict() if self.book else None
        }

    def __repr__(self):
        return f'<CollectionItem collection={self.collection_id} book={self.book_id} pos={self.position}>'
