from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.services.recommendation_service import get_recommendations_for_user

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommendations')
@login_required
def index():
    """Personalized explainable recommendation feed with score breakdowns."""
    include_wishlist = request.args.get('wishlist', 'true').lower() == 'true'
    include_reading = request.args.get('reading', 'false').lower() == 'true'

    recs_result = get_recommendations_for_user(
        user_id=current_user.id,
        limit=24,
        include_wishlist=include_wishlist,
        include_reading=include_reading
    )

    return render_template(
        'recommendations/index.html',
        recommendations=recs_result['recommendations'],
        total_eligible=recs_result['total_eligible'],
        is_onboarding_needed=recs_result['is_onboarding_needed'],
        preference=current_user.preference,
        include_wishlist=include_wishlist,
        include_reading=include_reading
    )
