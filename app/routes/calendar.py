import calendar
from datetime import datetime, timezone
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.services.statistics_service import StatisticsService

calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/calendar')
@login_required
def index():
    """Reading calendar and streak tracking."""
    now = datetime.now(timezone.utc)
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)

    # Bound check month
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    streaks = StatisticsService.get_user_streaks(current_user.id)
    days_data = StatisticsService.get_calendar_heatmap(current_user.id, year, month)
    
    month_name = calendar.month_name[month]
    first_weekday, num_days = calendar.monthrange(year, month)  # Monday=0, Sunday=6

    return render_template(
        'productivity/calendar.html',
        streaks=streaks,
        days_data=days_data,
        year=year,
        month=month,
        month_name=month_name,
        first_weekday=first_weekday,
        num_days=num_days
    )
