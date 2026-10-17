import pytest
from app.models.session import ReadingSession
from app.models.activity import ReadingActivity
from app.services.session_service import SessionService
from app.services.statistics_service import StatisticsService


def test_session_logging_and_deduplication(db, test_user):
    # Log session with idempotency token
    token = "test-token-12345"
    res1 = SessionService.log_reading_session(
        user_id=test_user.id,
        duration_seconds=1200,  # 20 mins
        notes="Engaging chapter",
        idempotency_token=token
    )
    assert res1['already_recorded'] is False
    assert ReadingSession.query.filter_by(user_id=test_user.id).count() == 1

    # Attempt duplicate submission with same token
    res2 = SessionService.log_reading_session(
        user_id=test_user.id,
        duration_seconds=1200,
        notes="Engaging chapter",
        idempotency_token=token
    )
    assert res2['already_recorded'] is True
    # Count remains 1
    assert ReadingSession.query.filter_by(user_id=test_user.id).count() == 1


def test_streak_calculation(db, test_user):
    # Before session, streaks should be 0
    streaks = StatisticsService.get_user_streaks(test_user.id)
    assert streaks['current_streak'] == 0

    # Log reading session today
    SessionService.log_reading_session(
        user_id=test_user.id,
        duration_seconds=900,  # 15 mins
        idempotency_token="streak-token-1"
    )

    streaks_after = StatisticsService.get_user_streaks(test_user.id)
    assert streaks_after['current_streak'] >= 1
    assert streaks_after['longest_streak'] >= 1
