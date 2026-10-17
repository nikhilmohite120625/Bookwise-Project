import re
from typing import Dict, Any, Optional
from app.models.book import Book
from app.models.reading import ReadingRecord
from app.models.preference import UserPreference
from app.services.recommendation_service import get_recommendations_for_user
from app.services.discovery_service import (
    get_mood_recommendations,
    find_books_by_reading_time,
    get_surprise_me_book,
    MOOD_MAPPINGS
)
from app.services.statistics_service import StatisticsService


class AssistantService:
    """Deterministic, rule-based reading assistant that answers queries with transparent rationale."""

    @classmethod
    def process_query(cls, user_id: Optional[int], message: str) -> Dict[str, Any]:
        text = message.strip().lower()
        if not text:
            return {
                'reply': "Greetings! I am your BookWise Atelier Reading Companion. How may I assist your literary journey today?",
                'suggestions': [
                    "What should I read next?",
                    "I have 30 minutes to read",
                    "Suggest a mysterious novel",
                    "How is my reading goal doing?"
                ],
                'books': []
            }

        # 1. Goal / Progress queries
        if any(w in text for w in ['goal', 'target', 'streak', 'progress', 'how am i doing']):
            if not user_id:
                return {
                    'reply': "Please log in to track your reading goals and habit streaks! Once logged in, I can report your progress against your annual target.",
                    'suggestions': ["What should I read next?", "Suggest a comforting book"],
                    'books': []
                }
            goals = StatisticsService.get_reading_goals(user_id)
            streaks = StatisticsService.get_user_streaks(user_id)
            reply = (
                f"📊 **Your {goals['year']} Reading Progress:**\n\n"
                f"- **Goal Target:** {goals['target']} books\n"
                f"- **Completed:** {goals['completed']} books ({goals['percent']}% achieved)\n"
                f"- **Remaining:** {goals['remaining']} books\n"
                f"- **Current Reading Streak:** {streaks['current_streak']} days 🔥 (Longest: {streaks['longest_streak']} days)\n\n"
                f"{'Keep the momentum going!' if goals['percent'] < 100 else 'Magnificent! You have fulfilled your reading target for the year!'}"
            )
            return {
                'reply': reply,
                'suggestions': ["What should I read next?", "I have 20 minutes to read", "Show my shelves"],
                'books': []
            }

        # 2. Time-based queries (e.g. "I have 30 minutes", "15 mins", "quick read")
        time_match = re.search(r'(\d+)\s*(?:min|minute|mins)', text)
        if time_match or 'quick' in text or 'short' in text or 'time' in text:
            target_minutes = int(time_match.group(1)) if time_match else 30
            books_data = find_books_by_reading_time(target_minutes, limit=3)
            books = [b['book'] for b in books_data]
            reply = (
                f"⏱️ **Curated for a {target_minutes}-minute session:**\n"
                f"I discovered {len(books)} books with estimated chapter/session paces closely aligned with your {target_minutes}-minute window."
            )
            return {
                'reply': reply,
                'books': [b.to_dict() for b in books],
                'suggestions': ["Suggest an adventurous story", "Surprise me with something unexpected"],
            }

        # 3. Mood-based queries
        for mood in MOOD_MAPPINGS.keys():
            if mood in text or mood[:-3] in text:  # e.g., 'myster' in 'mysterious'
                mood_res = get_mood_recommendations(mood, limit=3)
                books = [item['book'] for item in mood_res['results']]
                reply = (
                    f"✨ **{mood_res['mood']} Selection:**\n"
                    f"{mood_res['tagline']}\n\n"
                    f"Selected based on matching themes and tonal keywords:"
                )
                return {
                    'reply': reply,
                    'books': [b.to_dict() for b in books],
                    'suggestions': ["Give me something thought-provoking", "What should I read next?"]
                }

        # 4. Currently Reading query
        if 'currently reading' in text or 'reading now' in text or 'my current book' in text:
            if not user_id:
                return {
                    'reply': "Please log in to review your current reading shelf.",
                    'suggestions': ["Browse popular books", "Surprise me"],
                    'books': []
                }
            records = ReadingRecord.query.filter_by(user_id=user_id, status='currently_reading').all()
            if not records:
                return {
                    'reply': "You currently have no books marked as 'Currently Reading'. Would you like a personalized recommendation to start your next chapter?",
                    'suggestions': ["What should I read next?", "Browse Catalogue"],
                    'books': []
                }
            books = [r.book for r in records if r.book]
            reply = f"📖 You have **{len(books)}** book(s) in progress right now:"
            return {
                'reply': reply,
                'books': [b.to_dict() for b in books],
                'suggestions': ["Log reading progress", "Check my reading streak"]
            }

        # 5. Surprise Me query
        if 'surprise' in text or 'random' in text or 'pick for me' in text:
            book = get_surprise_me_book(user_id)
            if book:
                reply = f"🎲 **Surprise Selection:** Here is a distinguished title from our collection: *{book.title}* by {book.author}."
                return {
                    'reply': reply,
                    'books': [book.to_dict()],
                    'suggestions': ["Another surprise please", "Why was this recommended?"]
                }

        # 6. Default recommendation query
        if any(w in text for w in ['recommend', 'next', 'suggest', 'what to read', 'good book', 'advice']):
            if user_id:
                recs_data = get_recommendations_for_user(user_id, limit=3)
                books = [r['book'] for r in recs_data['recommendations']]
                if books:
                    reply = (
                        "📚 **Personalized Recommendation:**\n"
                        "Here are the top matches from our 100-point explainable recommendation engine, scored against your genres, language, suitability, and duration preferences:"
                    )
                    return {
                        'reply': reply,
                        'books': [b.to_dict() for b in books],
                        'suggestions': ["Explain the scoring", "I have 45 minutes to read", "Suggest something inspiring"]
                    }

            # Fallback for guest or without preferences
            popular = Book.query.order_by(Book.rating.desc()).limit(3).all()
            reply = (
                "📚 **Distinguished Selections:**\n"
                "Here are three highly acclaimed volumes from the BookWise Atelier. (Log in and configure your reading profile for personalized compatibility scores!)"
            )
            return {
                'reply': reply,
                'books': [b.to_dict() for b in popular],
                'suggestions': ["I have 30 minutes to read", "Suggest a mystery novel", "Surprise me"]
            }

        # Fallback response
        return {
            'reply': (
                "I am your BookWise literary assistant. I can guide your reading decisions, "
                "filter books by session duration, find specific moods (mysterious, inspiring, adventurous, comforting), "
                "or report your reading streak and annual goal."
            ),
            'suggestions': [
                "What should I read next?",
                "I have 30 minutes to read",
                "Suggest an inspiring biography",
                "How is my reading goal doing?"
            ],
            'books': []
        }
