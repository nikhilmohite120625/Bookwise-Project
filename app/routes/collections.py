from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.book import Book
from app.services.collection_service import CollectionService
from app.forms import CollectionForm

collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/collections', methods=['GET', 'POST'])
@login_required
def index():
    """Lists user collections and allows creating new collections."""
    form = CollectionForm()
    if form.validate_on_submit():
        CollectionService.create_collection(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data
        )
        flash(f'Collection "{form.name.data}" created!', 'success')
        return redirect(url_for('collections.index'))

    user_collections = CollectionService.get_user_collections(current_user.id)
    return render_template('productivity/collections.html', collections=user_collections, form=form)


@collections_bp.route('/collections/<int:collection_id>')
@login_required
def detail(collection_id: int):
    """Collection detail page displaying books in collection."""
    collection = CollectionService.get_collection(collection_id=collection_id, user_id=current_user.id)
    all_books = Book.query.order_by(Book.title.asc()).all()
    return render_template('productivity/collection_detail.html', collection=collection, all_books=all_books)


@collections_bp.route('/collections/<int:collection_id>/add-book', methods=['POST'])
@login_required
def add_book(collection_id: int):
    """Adds a book to a personal collection."""
    book_id = request.form.get('book_id', type=int)
    if book_id:
        CollectionService.add_book_to_collection(collection_id=collection_id, user_id=current_user.id, book_id=book_id)
        flash('Book added to collection.', 'success')
    return redirect(url_for('collections.detail', collection_id=collection_id))


@collections_bp.route('/collections/<int:collection_id>/remove-book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(collection_id: int, book_id: int):
    """Removes a book from a collection."""
    CollectionService.remove_book_from_collection(collection_id=collection_id, user_id=current_user.id, book_id=book_id)
    flash('Book removed from collection.', 'info')
    return redirect(url_for('collections.detail', collection_id=collection_id))


@collections_bp.route('/collections/<int:collection_id>/delete', methods=['POST'])
@login_required
def delete(collection_id: int):
    """Deletes an entire collection."""
    CollectionService.delete_collection(collection_id=collection_id, user_id=current_user.id)
    flash('Collection deleted.', 'info')
    return redirect(url_for('collections.index'))
