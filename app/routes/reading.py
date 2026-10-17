from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.reading import ReadingRecord
from app.models.wishlist import Wishlist
from app.models.book import Book
from app.services.reading_service import ReadingService
from app.services.statistics_service import StatisticsService
from app.forms import ReadingRecordForm

reading_bp = Blueprint('reading', __name__)


@reading_bp.route('/my-books')
@login_required
def my_books():
    """User personal reading shelves (Want to Read, Currently Reading, Completed)."""
    active_tab = request.args.get('shelf', 'currently_reading')

    want_to_read = ReadingService.get_user_shelf(current_user.id, 'want_to_read')
    currently_reading = ReadingService.get_user_shelf(current_user.id, 'currently_reading')
    completed = ReadingService.get_user_shelf(current_user.id, 'completed')

    stats_summary = StatisticsService.get_dashboard_summary(current_user.id)

    return render_template(
        'reading/my_books.html',
        want_to_read=want_to_read,
        currently_reading=currently_reading,
        completed=completed,
        active_tab=active_tab,
        stats_summary=stats_summary
    )


@reading_bp.route('/my-books/set-status', methods=['POST'])
@login_required
def set_status():
    """Adds or moves a book to a shelf."""
    book_id = request.form.get('book_id', type=int)
    status = request.form.get('status', 'want_to_read')
    pages_read = request.form.get('pages_read', type=int)
    personal_rating = request.form.get('personal_rating', type=float)
    notes = request.form.get('notes')

    if not book_id:
        flash('Invalid book selection.', 'danger')
        return redirect(url_for('reading.my_books'))

    try:
        ReadingService.set_shelf_status(
            user_id=current_user.id,
            book_id=book_id,
            status=status,
            pages_read=pages_read,
            personal_rating=personal_rating,
            notes=notes
        )
        # If moving to reading or completed, remove from wishlist if present
        if status in ['currently_reading', 'completed']:
            wish = Wishlist.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            if wish:
                db.session.delete(wish)
                db.session.commit()

        flash(f'Book moved to {status.replace("_", " ").title()} shelf.', 'success')
    except Exception as e:
        flash(f'Could not update shelf: {str(e)}', 'danger')

    next_url = request.form.get('next') or request.referrer or url_for('reading.my_books', shelf=status)
    return redirect(next_url)


@reading_bp.route('/my-books/update-progress', methods=['POST'])
@login_required
def update_progress():
    """Updates reading progress for currently reading books."""
    book_id = request.form.get('book_id', type=int)
    pages_read = request.form.get('pages_read', type=int)
    notes = request.form.get('notes')

    if not book_id or pages_read is None:
        flash('Invalid progress data.', 'danger')
        return redirect(url_for('reading.my_books'))

    try:
        record = ReadingService.update_progress(
            user_id=current_user.id,
            book_id=book_id,
            pages_read=pages_read,
            notes=notes
        )
        if record.status == 'completed':
            flash(f'Congratulations on finishing "{record.book.title}"!', 'success')
        else:
            flash(f'Progress updated to page {record.pages_read}.', 'success')
    except Exception as e:
        flash(f'Error updating progress: {str(e)}', 'danger')

    return redirect(request.form.get('next') or url_for('reading.my_books', shelf='currently_reading'))


@reading_bp.route('/my-books/remove', methods=['POST'])
@login_required
def remove_book():
    """Removes a book from the user's shelf."""
    book_id = request.form.get('book_id', type=int)
    if book_id:
        ReadingService.remove_from_shelf(current_user.id, book_id)
        flash('Book removed from your shelf.', 'info')
    return redirect(request.referrer or url_for('reading.my_books'))


@reading_bp.route('/my-books/queue')
@login_required
def queue():
    """Reading priority queue view for Want to Read books."""
    queue_records = ReadingService.get_user_shelf(current_user.id, 'want_to_read')
    return render_template('reading/queue.html', queue_records=queue_records)


@reading_bp.route('/wishlist')
@login_required
def wishlist():
    """User wishlist view."""
    items = Wishlist.query.filter_by(user_id=current_user.id).order_by(Wishlist.added_at.desc()).all()
    return render_template('reading/wishlist.html', wishlist_items=items)


@reading_bp.route('/wishlist/toggle/<int:book_id>', methods=['POST'])
@login_required
def toggle_wishlist(book_id: int):
    """Toggles a book in/out of the user's wishlist."""
    Book.query.get_or_404(book_id)
    existing = Wishlist.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Book removed from your Wishlist.', 'info')
    else:
        new_item = Wishlist(user_id=current_user.id, book_id=book_id)
        db.session.add(new_item)
        db.session.commit()
        flash('Book added to your Wishlist.', 'success')

    return redirect(request.referrer or url_for('reading.wishlist'))
