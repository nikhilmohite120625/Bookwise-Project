from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.book import Book
from app.services.journal_service import JournalService
from app.forms import JournalForm

journal_bp = Blueprint('journal', __name__)


@journal_bp.route('/journal', methods=['GET', 'POST'])
@login_required
def index():
    """Private reading journal reflections."""
    form = JournalForm()
    user_books = Book.query.order_by(Book.title.asc()).all()
    form.book_id.choices = [(0, '— General Reflection (No Specific Book) —')] + [(b.id, f"{b.title} by {b.author}") for b in user_books]

    if form.validate_on_submit():
        book_id = form.book_id.data if form.book_id.data != 0 else None
        JournalService.create_entry(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            book_id=book_id
        )
        flash('Reading reflection saved to your private journal.', 'success')
        return redirect(url_for('journal.index'))

    entries = JournalService.get_user_entries(current_user.id)
    return render_template('productivity/journal.html', form=form, entries=entries)


@journal_bp.route('/journal/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id: int):
    """Deletes a journal entry safely."""
    JournalService.delete_entry(entry_id=entry_id, user_id=current_user.id)
    flash('Journal reflection removed.', 'info')
    return redirect(url_for('journal.index'))
