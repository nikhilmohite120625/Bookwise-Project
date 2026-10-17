from datetime import datetime, timezone
from typing import List, Optional
from app.extensions import db
from app.models.collection import PersonalCollection, CollectionItem
from app.models.book import Book


class CollectionService:

    @staticmethod
    def get_user_collections(user_id: int) -> List[PersonalCollection]:
        """Returns all collections owned by user."""
        return PersonalCollection.query.filter_by(user_id=user_id).order_by(PersonalCollection.created_at.desc()).all()

    @staticmethod
    def get_collection(collection_id: int, user_id: int) -> PersonalCollection:
        """Gets a specific collection, enforcing user ownership."""
        return PersonalCollection.query.filter_by(id=collection_id, user_id=user_id).first_or_404()

    @staticmethod
    def create_collection(user_id: int, name: str, description: Optional[str] = None) -> PersonalCollection:
        """Creates a new personal curated collection."""
        coll = PersonalCollection(
            user_id=user_id,
            name=name.strip(),
            description=description.strip() if description else None
        )
        db.session.add(coll)
        db.session.commit()
        return coll

    @staticmethod
    def add_book_to_collection(collection_id: int, user_id: int, book_id: int) -> CollectionItem:
        """Adds a book to a collection, preventing duplicates and setting position."""
        coll = PersonalCollection.query.filter_by(id=collection_id, user_id=user_id).first_or_404()
        Book.query.get_or_404(book_id)

        existing = CollectionItem.query.filter_by(collection_id=coll.id, book_id=book_id).first()
        if existing:
            return existing

        max_pos = db.session.query(db.func.max(CollectionItem.position)).filter_by(collection_id=coll.id).scalar() or 0
        item = CollectionItem(
            collection_id=coll.id,
            book_id=book_id,
            position=max_pos + 1
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def remove_book_from_collection(collection_id: int, user_id: int, book_id: int) -> bool:
        """Removes a book from a collection."""
        coll = PersonalCollection.query.filter_by(id=collection_id, user_id=user_id).first_or_404()
        item = CollectionItem.query.filter_by(collection_id=coll.id, book_id=book_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_collection(collection_id: int, user_id: int) -> bool:
        """Deletes an entire collection and its items."""
        coll = PersonalCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if coll:
            db.session.delete(coll)
            db.session.commit()
            return True
        return False
