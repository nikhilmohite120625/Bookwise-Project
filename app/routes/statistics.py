from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.goal import ReadingGoal
from app.services.statistics_service import StatisticsService
from app.forms import ReadingGoalForm

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/statistics', methods=['GET', 'POST'])
@login_required
def index():
    """Reading Analytics, Pacing, and Goal Management."""
    now = datetime.now(timezone.utc)
    current_year = now.year

    goal_form = ReadingGoalForm()
    user_goal = ReadingGoal.query.filter_by(user_id=current_user.id, goal_year=current_year).first()

    if goal_form.validate_on_submit():
        if not user_goal:
            user_goal = ReadingGoal(
                user_id=current_user.id,
                goal_year=goal_form.goal_year.data,
                target_books=goal_form.target_books.data,
                monthly_target=goal_form.monthly_target.data
            )
            db.session.add(user_goal)
        else:
            user_goal.target_books = goal_form.target_books.data
            user_goal.monthly_target = goal_form.monthly_target.data
        db.session.commit()
        flash('Annual reading goal updated successfully.', 'success')
        return redirect(url_for('statistics.index'))

    if request.method == 'GET' and user_goal:
        goal_form.target_books.data = user_goal.target_books
        goal_form.goal_year.data = user_goal.goal_year
        goal_form.monthly_target.data = user_goal.monthly_target
    elif request.method == 'GET':
        goal_form.target_books.data = 12
        goal_form.goal_year.data = current_year

    summary = StatisticsService.get_dashboard_summary(current_user.id)
    monthly_data = StatisticsService.get_monthly_activity(current_user.id, current_year)
    genre_data = StatisticsService.get_genre_distribution(current_user.id)

    return render_template(
        'statistics/index.html',
        summary=summary,
        monthly_data=monthly_data,
        genre_data=genre_data,
        goal_form=goal_form,
        current_year=current_year
    )
