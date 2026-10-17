from datetime import date, datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import func, extract
from app.models.activity import ReadingActivity
from app.models.reading import ReadingRecord
from app.models.goal import ReadingGoal
from app.models.book import Book


class StatisticsService:

    @staticmethod
    def get_user_streaks(user_id: int) -> Dict[str, int]:
        """Calculates current streak and all-time longest streak in days."""
        activities = ReadingActivity.query.filter_by(user_id=user_id).order_by(ReadingActivity.activity_date.asc()).all()
        if not activities:
            return {'current_streak': 0, 'longest_streak': 0}

        active_dates = {
            a.activity_date for a in activities
            if (a.minutes_read > 0 or a.pages_read > 0 or a.sessions_count > 0 or a.books_completed > 0)
        }

        if not active_dates:
            return {'current_streak': 0, 'longest_streak': 0}

        sorted_dates = sorted(list(active_dates))

        # Calculate longest streak
        longest = 0
        current_run = 0
        prev_date = None

        for d in sorted_dates:
            if prev_date is None or d == prev_date + timedelta(days=1):
                current_run += 1
            else:
                current_run = 1
            if current_run > longest:
                longest = current_run
            prev_date = d

        # Calculate current streak
        today = date.today()
        yesterday = today - timedelta(days=1)

        current_streak = 0
        check_date = today if today in active_dates else (yesterday if yesterday in active_dates else None)

        if check_date:
            while check_date in active_dates:
                current_streak += 1
                check_date = check_date - timedelta(days=1)

        return {
            'current_streak': current_streak,
            'longest_streak': max(longest, current_streak)
        }

    @staticmethod
    def get_reading_goals(user_id: int, year: Optional[int] = None) -> Dict[str, Any]:
        """Calculates progress towards annual reading target."""
        target_year = year or datetime.now(timezone.utc).year
        goal = ReadingGoal.query.filter_by(user_id=user_id, goal_year=target_year).first()

        completed_records = ReadingRecord.query.filter(
            ReadingRecord.user_id == user_id,
            ReadingRecord.status == 'completed',
            extract('year', ReadingRecord.completed_at) == target_year
        ).all()

        completed_count = len(completed_records)
        target = goal.target_books if goal else 12
        pct = int(min(100, (completed_count / target) * 100)) if target > 0 else 0

        return {
            'year': target_year,
            'target': target,
            'completed': completed_count,
            'percent': pct,
            'remaining': max(0, target - completed_count),
            'goal_exists': goal is not None
        }

    @staticmethod
    def get_genre_distribution(user_id: int) -> Dict[str, int]:
        """Calculates genre breakdown of all books on user's shelves."""
        records = ReadingRecord.query.filter_by(user_id=user_id).all()
        genre_counts: Dict[str, int] = {}

        for rec in records:
            if rec.book:
                for g in rec.book.genres_list:
                    clean = g.strip().title()
                    genre_counts[clean] = genre_counts.get(clean, 0) + 1

        return dict(sorted(genre_counts.items(), key=lambda x: -x[1])[:8])

    @staticmethod
    def get_monthly_activity(user_id: int, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns monthly breakdown of books read and minutes logged for given year."""
        target_year = year or datetime.now(timezone.utc).year
        months_data = []

        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for month_idx in range(1, 13):
            # Books completed in this month
            books_count = ReadingRecord.query.filter(
                ReadingRecord.user_id == user_id,
                ReadingRecord.status == 'completed',
                extract('year', ReadingRecord.completed_at) == target_year,
                extract('month', ReadingRecord.completed_at) == month_idx
            ).count()

            # Minutes read in this month
            minutes_sum = ReadingActivity.query.filter(
                ReadingActivity.user_id == user_id,
                extract('year', ReadingActivity.activity_date) == target_year,
                extract('month', ReadingActivity.activity_date) == month_idx
            ).with_entities(func.sum(ReadingActivity.minutes_read)).scalar() or 0

            months_data.append({
                'month': month_names[month_idx - 1],
                'month_num': month_idx,
                'books': books_count,
                'minutes': int(minutes_sum)
            })

        return months_data

    @staticmethod
    def get_calendar_heatmap(user_id: int, year: int, month: int) -> List[Dict[str, Any]]:
        """Generates daily activity data for a given month and year for calendar rendering."""
        activities = ReadingActivity.query.filter(
            ReadingActivity.user_id == user_id,
            extract('year', ReadingActivity.activity_date) == year,
            extract('month', ReadingActivity.activity_date) == month
        ).all()

        activity_map = {a.activity_date.day: a for a in activities}
        # Days in month
        import calendar
        num_days = calendar.monthrange(year, month)[1]

        days_data = []
        for day in range(1, num_days + 1):
            act = activity_map.get(day)
            days_data.append({
                'day': day,
                'minutes': act.minutes_read if act else 0,
                'pages': act.pages_read if act else 0,
                'books': act.books_completed if act else 0,
                'has_activity': bool(act and (act.minutes_read > 0 or act.pages_read > 0 or act.books_completed > 0))
            })

        return days_data

    @staticmethod
    def get_dashboard_summary(user_id: int) -> Dict[str, Any]:
        """Aggregates all key metrics for the user dashboard."""
        streaks = StatisticsService.get_user_streaks(user_id)
        goals = StatisticsService.get_reading_goals(user_id)
        
        want_count = ReadingRecord.query.filter_by(user_id=user_id, status='want_to_read').count()
        reading_count = ReadingRecord.query.filter_by(user_id=user_id, status='currently_reading').count()
        completed_count = ReadingRecord.query.filter_by(user_id=user_id, status='completed').count()

        total_pages = ReadingActivity.query.filter_by(user_id=user_id).with_entities(func.sum(ReadingActivity.pages_read)).scalar() or 0
        total_minutes = ReadingActivity.query.filter_by(user_id=user_id).with_entities(func.sum(ReadingActivity.minutes_read)).scalar() or 0

        currently_reading_books = ReadingRecord.query.filter_by(
            user_id=user_id,
            status='currently_reading'
        ).order_by(ReadingRecord.updated_at.desc()).limit(3).all()

        return {
            'streaks': streaks,
            'goals': goals,
            'shelf_counts': {
                'want_to_read': want_count,
                'currently_reading': reading_count,
                'completed': completed_count,
                'total': want_count + reading_count + completed_count
            },
            'total_pages': int(total_pages),
            'total_hours': round(total_minutes / 60, 1),
            'currently_reading': currently_reading_books
        }
