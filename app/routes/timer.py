from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.reading import ReadingRecord
from app.services.session_service import SessionService

timer_bp = Blueprint('timer', __name__)


@timer_bp.route('/timer')
@login_required
def index():
    """Live interactive reading timer & stopwatch companion."""
    selected_book_id = request.args.get('book_id', type=int)
    currently_reading = ReadingRecord.query.filter_by(
        user_id=current_user.id,
        status='currently_reading'
    ).all()

    return render_template(
        'productivity/timer.html',
        currently_reading=currently_reading,
        selected_book_id=selected_book_id
    )


@timer_bp.route('/timer/save-session', methods=['POST'])
@login_required
def save_session():
    """Saves a finished timer session with deduplication safeguard."""
    duration_seconds = request.form.get('duration_seconds', type=int)
    book_id = request.form.get('book_id', type=int)
    pages_read = request.form.get('pages_read', type=int)
    notes = request.form.get('notes')
    token = request.form.get('idempotency_token')

    if not duration_seconds or duration_seconds <= 0:
        flash('Session duration was too brief to record.', 'warning')
        return redirect(url_for('timer.index'))

    try:
        result = SessionService.log_reading_session(
            user_id=current_user.id,
            duration_seconds=duration_seconds,
            book_id=book_id,
            notes=notes,
            pages_read=pages_read,
            idempotency_token=token
        )
        if result['already_recorded']:
            flash('This reading session was already saved.', 'info')
        else:
            flash(f'Brilliant! Logged {result["session"].duration_minutes} minutes of dedicated reading.', 'success')
    except Exception as e:
        flash(f'Could not save reading session: {str(e)}', 'danger')

    return redirect(url_for('calendar.index'))
