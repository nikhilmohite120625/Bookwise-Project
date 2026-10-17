import html
import os
import streamlit as st
from datetime import datetime, timezone

# -----------------------------------------------------------------------------
# 1. Page Configuration & Atelier Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BookWise — The Reading Atelier",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for The Reading Atelier Design System
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --atelier-ivory: #fbf8f3;
    --atelier-parchment: #f4eee0;
    --atelier-forest: #1a3c2e;
    --atelier-navy: #0f172a;
    --atelier-gold: #c5a059;
    --atelier-gold-light: #e8d7b5;
    --atelier-muted: #6b7280;
    --atelier-card-bg: #ffffff;
    --atelier-border: rgba(197, 160, 89, 0.25);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a3c2e;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', Georgia, serif;
    color: #1a3c2e;
    font-weight: 700;
}

.atelier-brand-header {
    background: linear-gradient(135deg, #1a3c2e 0%, #0f172a 100%);
    color: #fbf8f3;
    padding: 2.2rem 2.5rem;
    border-radius: 14px;
    border: 1px solid #c5a059;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
}

.atelier-brand-header h1 {
    font-family: 'Cinzel', serif;
    color: #c5a059;
    margin: 0;
    font-size: 2.4rem;
    letter-spacing: 2px;
}

.atelier-brand-header p {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-style: italic;
    margin-top: 0.5rem;
    margin-bottom: 0;
}

.book-card {
    background: #ffffff;
    border: 1px solid rgba(197, 160, 89, 0.3);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.book-card:hover {
    box-shadow: 0 8px 24px rgba(197, 160, 89, 0.18);
    transform: translateY(-2px);
}

.score-badge {
    display: inline-block;
    background: #1a3c2e;
    color: #c5a059;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    border: 1px solid #c5a059;
}

.genre-tag {
    display: inline-block;
    background: #f4eee0;
    color: #1a3c2e;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
    border: 1px solid rgba(197, 160, 89, 0.3);
}

.stat-card {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid rgba(197, 160, 89, 0.3);
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.stat-number {
    font-family: 'Cinzel', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #c5a059;
}

.stat-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6b7280;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Flask Application Context & Database Bridge
# -----------------------------------------------------------------------------
@st.cache_resource
def init_application():
    """Initializes the Flask app context and verifies schema & seed catalogue."""
    from app import create_app
    from app.extensions import db
    from seeds.sample_books import seed_database
    from app.models.book import Book

    app = create_app('development')
    with app.app_context():
        db.create_all()
        # Seed catalogue if empty
        if Book.query.count() == 0:
            seed_database(db)
    return app


flask_app = init_application()
from app.extensions import db
from app.models.book import Book
from app.models.user import User
from app.models.preference import UserPreference
from app.models.reading import ReadingRecord
from app.models.wishlist import Wishlist
from app.models.goal import ReadingGoal
from app.models.activity import ReadingActivity


# -----------------------------------------------------------------------------
# 3. Session State & Authentication
# -----------------------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'guest'


def login_user(user):
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_name = user.name
    st.session_state.user_email = user.email
    st.session_state.user_role = user.role


def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.user_role = 'guest'
    st.rerun()


# -----------------------------------------------------------------------------
# 4. Sidebar: Authentication, Navigation & Reader Profile
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏛️ BookWise Atelier")
    st.caption("Find Your Next Favourite Book.")
    st.markdown("---")

    with flask_app.app_context():
        from app.models.user import User
        from app.models.preference import UserPreference
        from app.extensions import db

        if st.session_state.logged_in:
            st.success(f"**Reader:** {st.session_state.user_name}")
            st.caption(f"Role: {st.session_state.user_role.upper()} | {st.session_state.user_email}")
            if st.button("Log Out", use_container_width=True):
                logout_user()
        else:
            auth_mode = st.radio("Access Mode", ["Guest / Quick Sign-In", "Register New Reader"], label_visibility="collapsed")
            
            if auth_mode == "Guest / Quick Sign-In":
                users = User.query.order_by(User.name.asc()).all()
                if users:
                    user_options = {f"{u.name} ({u.email}) [{u.role}]": u.id for u in users}
                    selected_label = st.selectbox("Select Reader Profile", list(user_options.keys()))
                    if st.button("Sign In as Selected Reader", type="primary", use_container_width=True):
                        selected_user = db.session.get(User, user_options[selected_label])
                        login_user(selected_user)
                        st.rerun()
                else:
                    st.info("No registered users yet. Create your account below.")

                with st.expander("Sign in with Password"):
                    in_email = st.text_input("Email", key="login_email")
                    in_password = st.text_input("Password", type="password", key="login_pwd")
                    if st.button("Sign In"):
                        user = User.query.filter_by(email=in_email.strip()).first()
                        if user and user.check_password(in_password):
                            login_user(user)
                            st.rerun()
                        else:
                            st.error("Invalid credentials.")

            else:
                st.markdown("#### New Reader Registration")
                reg_name = st.text_input("Full Name", key="reg_name")
                reg_email = st.text_input("Email Address", key="reg_email")
                reg_password = st.text_input("Password (min 8 chars)", type="password", key="reg_pwd")
                if st.button("Create Atelier Account", type="primary", use_container_width=True):
                    if not reg_name or not reg_email or not reg_password:
                        st.error("Please fill in all fields.")
                    elif len(reg_password) < 8:
                        st.error("Password must be at least 8 characters.")
                    elif User.query.filter_by(email=reg_email.strip()).first():
                        st.error("Email address is already registered.")
                    else:
                        new_user = User(
                            name=reg_name.strip(),
                            email=reg_email.strip(),
                            role='user'
                        )
                        new_user.set_password(reg_password)
                        db.session.add(new_user)
                        db.session.flush()

                        pref = UserPreference(
                            user_id=new_user.id,
                            preferred_genres=["Fiction", "Philosophy"],
                            preferred_languages=["English"],
                            age_preference="Adult",
                            preferred_duration=30,
                            interest_keywords=["wisdom", "discovery", "ideas"],
                            onboarding_completed=True,
                            theme_preference="light"
                        )
                        db.session.add(pref)
                        db.session.commit()
                        login_user(new_user)
                        st.success("Account created successfully!")
                        st.rerun()

    st.markdown("---")
    menu = st.radio(
        "Navigation",
        [
            "📚 Catalogue & Search",
            "🔮 Explainable Recommendations",
            "🧭 Mood & Time Discovery",
            "📖 My Reading Shelves",
            "🤍 Wishlist",
            "📊 Reading Analytics & Goals",
            "⚙️ Reader Preferences"
        ]
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #6b7280; text-align: center;">
            BookWise Reading Atelier &copy; 2026<br>
            Powered by Streamlit & SQLAlchemy
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------------------------------------------------------
# 5. Header Banner
# -----------------------------------------------------------------------------
st.markdown("""
<div class="atelier-brand-header">
    <h1>BOOKWISE ATELIER</h1>
    <p>A premium digital reading companion and explainable book recommendation sanctuary.</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. Helper: Render Book Card
# -----------------------------------------------------------------------------
def render_book_cover(book):
    """Renders either an image or the inline Atelier SVG fallback."""
    if book.cover_url and book.cover_url.startswith("http"):
        st.image(book.cover_url, use_column_width=True)
    else:
        st.markdown(
            f'<div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">{book.get_fallback_svg()}</div>',
            unsafe_allow_html=True
        )


def add_to_wishlist(user_id: int, book_id: int):
    item = Wishlist.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not item:
        item = Wishlist(user_id=user_id, book_id=book_id)
        db.session.add(item)
        db.session.commit()
    return item


def remove_from_wishlist(user_id: int, book_id: int):
    item = Wishlist.query.filter_by(user_id=user_id, book_id=book_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False


def shelf_action_buttons(book_id, key_prefix):
    """Renders action buttons to move a book to shelves or wishlist."""
    with flask_app.app_context():
        from app.services.reading_service import ReadingService

        if not st.session_state.logged_in:
            st.caption("Sign in to save books to shelves or wishlist.")
            return

        user_id = st.session_state.user_id
        current_record = ReadingRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
        is_wishlisted = bool(Wishlist.query.filter_by(user_id=user_id, book_id=book_id).first())

        status_text = f"Current Shelf: **{current_record.status.replace('_', ' ').title()}**" if current_record else "Not in shelves"
        st.markdown(f"<small>{status_text}</small>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📖 Read Next", key=f"{key_prefix}_wtr_{book_id}", help="Add to Want to Read"):
                ReadingService.set_shelf_status(user_id=user_id, book_id=book_id, status="want_to_read")
                st.toast("Added to 'Want to Read' shelf!")
                st.rerun()
        with col2:
            if st.button("⏳ Reading", key=f"{key_prefix}_cr_{book_id}", help="Set as Currently Reading"):
                ReadingService.set_shelf_status(user_id=user_id, book_id=book_id, status="currently_reading")
                st.toast("Set to 'Currently Reading'!")
                st.rerun()
        with col3:
            if st.button("✅ Done", key=f"{key_prefix}_done_{book_id}", help="Mark as Completed"):
                ReadingService.set_shelf_status(user_id=user_id, book_id=book_id, status="completed")
                st.toast("Marked as Completed!")
                st.rerun()
        with col4:
            if is_wishlisted:
                if st.button("💔 Saved", key=f"{key_prefix}_unwish_{book_id}", help="Remove from Wishlist"):
                    remove_from_wishlist(user_id=user_id, book_id=book_id)
                    st.toast("Removed from Wishlist.")
                    st.rerun()
            else:
                if st.button("🤍 Wishlist", key=f"{key_prefix}_wish_{book_id}", help="Add to Wishlist"):
                    add_to_wishlist(user_id=user_id, book_id=book_id)
                    st.toast("Added to Wishlist!")
                    st.rerun()


# -----------------------------------------------------------------------------
# 7. Page: Catalogue & Search
# -----------------------------------------------------------------------------
if menu == "📚 Catalogue & Search":
    st.markdown("## 📚 The BookWise Catalogue")
    st.write("Browse curated volumes from our atelier collection across 15+ genres.")

    with flask_app.app_context():
        from app.models.book import Book
        from app.forms import ALL_GENRES

        # Search and filters
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.2, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search by title, author, or keywords", placeholder="e.g. Marcus Aurelius, Magic, Philosophy...")
        with f_col2:
            selected_genre = st.selectbox("Genre Filter", ["All Genres"] + ALL_GENRES)
        with f_col3:
            selected_age = st.selectbox("Suitability", ["All", "All Ages", "Young Adult", "Adult", "Mature"])
        with f_col4:
            min_rating = st.slider("Min Rating", 3.0, 5.0, 3.5, 0.1)

        # Base query
        query = Book.query.filter(Book.rating >= min_rating)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(Book.title.ilike(term) | Book.author.ilike(term) | Book.description.ilike(term))
        if selected_age != "All":
            query = query.filter(Book.age_suitability == selected_age)

        books = query.order_by(Book.rating.desc(), Book.title.asc()).all()

        # Genre post-filter (since genres is stored as JSON array)
        if selected_genre != "All Genres":
            books = [b for b in books if selected_genre.lower() in [g.lower() for g in b.genres_list]]

        st.caption(f"Displaying **{len(books)}** curated volumes matching your criteria.")

        # Grid of books
        for idx in range(0, len(books), 2):
            row_books = books[idx:idx+2]
            cols = st.columns(2)
            for c_idx, book in enumerate(row_books):
                with cols[c_idx]:
                    st.markdown(f"""
                    <div class="book-card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <h3 style="margin: 0; font-size: 1.3rem;">{html.escape(book.title)}</h3>
                                <div style="color: #6b7280; font-size: 0.95rem; font-style: italic; margin-top: 2px;">
                                    by {html.escape(book.author)} ({book.publication_year or 'N/A'})
                                </div>
                            </div>
                            <span class="score-badge">⭐ {book.rating:.1f}</span>
                        </div>
                        <div style="margin-top: 0.75rem;">
                            {' '.join([f'<span class="genre-tag">{html.escape(g)}</span>' for g in book.genres_list])}
                        </div>
                        <div style="margin: 0.6rem 0; font-size: 0.85rem; color: #4b5563;">
                            ⏱️ ~{book.estimated_duration or 30} mins reading pace &nbsp;|&nbsp; 📖 {book.page_count or 'N/A'} pages &nbsp;|&nbsp; 🏷️ {book.age_suitability}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("📖 View Synopsis & Manage Shelf"):
                        c_img, c_desc = st.columns([1, 2.5])
                        with c_img:
                            render_book_cover(book)
                        with c_desc:
                            st.write(book.description or "No synopsis available.")
                            if book.keywords_list:
                                st.caption("Themes: " + ", ".join(book.keywords_list))
                            st.markdown("---")
                            shelf_action_buttons(book.id, f"cat_{book.id}")


# -----------------------------------------------------------------------------
# 8. Page: Explainable Recommendations
# -----------------------------------------------------------------------------
elif menu == "🔮 Explainable Recommendations":
    st.markdown("## 🔮 Explainable 100-Point Recommendations")
    st.write(
        "Our transparent, deterministic algorithm evaluates every candidate book across 5 distinct dimensions: "
        "**Genre (40 pts)**, **Language (20 pts)**, **Age Suitability (15 pts)**, **Duration Pace (15 pts)**, and **Keywords (10 pts)**."
    )

    if not st.session_state.logged_in:
        st.warning("Please sign in or select a reader profile in the sidebar to generate personalized recommendations.")
    else:
        with flask_app.app_context():
            from app.services.recommendation_service import get_recommendations_for_user
            from app.models.user import User

            user = db.session.get(User, st.session_state.user_id)
            recs_data = get_recommendations_for_user(user_id=user.id, limit=12)

            if recs_data.get('is_onboarding_needed'):
                st.info("💡 Your reader profile has not specified preferred genres or keywords yet. Set them in **Reader Preferences** to unlock 100-point tailored scoring!")

            recommendations = recs_data['recommendations']
            st.caption(f"Evaluated candidate catalogue. Found **{recs_data['total_eligible']}** eligible books. Showing top **{len(recommendations)}** matches.")

            for item in recommendations:
                book = item['book']
                total_score = item['total_score']
                scores = {
                    'Genre': (item['genre_score'], 40),
                    'Language': (item['language_score'], 20),
                    'Age Suitability': (item['age_score'], 15),
                    'Duration Pace': (item['duration_score'], 15),
                    'Interest Keywords': (item['interest_score'], 10)
                }

                st.markdown(f"""
                <div class="book-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="margin: 0; font-size: 1.35rem;">{html.escape(book.title)}</h3>
                            <div style="color: #6b7280; font-style: italic;">by {html.escape(book.author)}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="score-badge" style="font-size: 1rem; padding: 0.35rem 0.8rem;">
                                {total_score:.1f} / 100
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_cov, col_breakdown = st.columns([1, 3])
                with col_cov:
                    render_book_cover(book)
                with col_breakdown:
                    st.markdown("#### 🎯 Score Breakdown")
                    for dim_name, (score, max_score) in scores.items():
                        pct = min(1.0, max(0.0, score / max_score)) if max_score > 0 else 0
                        st.write(f"**{dim_name}**: `{score:.1f} / {max_score}` pts")
                        st.progress(pct)

                    with st.expander("🔍 Why this book? (Detailed Explainability)"):
                        st.markdown("**Matching Rationale:**")
                        for r in item['reasons']:
                            st.markdown(f"- {r}")

                        if item['matched_genres']:
                            st.write(f"**Matched Genres:** {', '.join(item['matched_genres'])}")
                        if item['matched_keywords']:
                            st.write(f"**Matched Keywords:** {', '.join(item['matched_keywords'])}")

                    shelf_action_buttons(book.id, f"rec_{book.id}")
                st.markdown("---")


# -----------------------------------------------------------------------------
# 9. Page: Mood & Time Discovery
# -----------------------------------------------------------------------------
elif menu == "🧭 Mood & Time Discovery":
    st.markdown("## 🧭 Discovery Atelier: Mood & Reading Time")
    st.write("Serendipitous discovery tailored to how you feel or how much time you have right now.")

    with flask_app.app_context():
        from app.services.discovery_service import MOOD_MAPPINGS, get_surprise_me_book, find_books_by_reading_time
        from app.models.book import Book

        tab_mood, tab_time, tab_surprise = st.tabs(["🎭 By Mood", "⏱️ By Reading Time", "🎲 Surprise Me"])

        with tab_mood:
            st.markdown("### How are you feeling today?")
            mood_names = list(MOOD_MAPPINGS.keys())
            cols = st.columns(3)
            selected_mood = None
            for idx, m_name in enumerate(mood_names):
                with cols[idx % 3]:
                    if st.button(f"{m_name.replace('-', ' ').title()}", key=f"mood_btn_{m_name}", use_container_width=True):
                        st.session_state['active_mood'] = m_name

            active_mood = st.session_state.get('active_mood', 'thought-provoking')
            mood_info = MOOD_MAPPINGS[active_mood]
            st.info(f"**{active_mood.title()}:** {mood_info['tagline']}")

            # Filter books matching mood genres and keywords
            matched_books = []
            for b in Book.query.all():
                book_genres = [g.lower() for g in b.genres_list]
                book_keywords = [k.lower() for k in b.keywords_list]
                has_genre = any(g in mood_info['genres'] for g in book_genres)
                has_kw = any(k in mood_info['keywords'] for k in book_keywords)
                if has_genre or has_kw:
                    matched_books.append(b)

            st.write(f"Found **{len(matched_books)}** books matching **{active_mood.title()}** mood:")
            for b in matched_books[:6]:
                st.markdown(f"**{b.title}** by *{b.author}* — ⭐ {b.rating:.1f}")
                shelf_action_buttons(b.id, f"mood_{b.id}")

        with tab_time:
            st.markdown("### How much time do you have to read?")
            time_choice = st.select_slider(
                "Available Reading Session (minutes):",
                options=[10, 20, 30, 45, 60],
                value=30
            )
            time_books = find_books_by_reading_time(available_minutes=time_choice, tolerance_minutes=15)
            st.write(f"Showing **{len(time_books)}** books aligned with a **~{time_choice} min** reading pace:")
            for b in time_books[:6]:
                st.markdown(f"**{b.title}** by *{b.author}* (Estimated: ~{b.estimated_duration} mins) — ⭐ {b.rating:.1f}")
                shelf_action_buttons(b.id, f"time_{b.id}")

        with tab_surprise:
            st.markdown("### Serendipitous Reading")
            st.write("Let the Atelier handpick an exceptional, unexpected book from the collection.")
            if st.button("🎲 Surprise Me!", type="primary"):
                user_id = st.session_state.user_id if st.session_state.logged_in else None
                surprise_book = get_surprise_me_book(user_id=user_id)
                if surprise_book:
                    st.success(f"**Your Atelier Selection:** {surprise_book.title} by {surprise_book.author}")
                    c_s1, c_s2 = st.columns([1, 2])
                    with c_s1:
                        render_book_cover(surprise_book)
                    with c_s2:
                        st.write(surprise_book.description)
                        st.write(f"**Genres:** {', '.join(surprise_book.genres_list)}")
                        st.write(f"**Pace:** ~{surprise_book.estimated_duration or 30} mins | **Pages:** {surprise_book.page_count}")
                        shelf_action_buttons(surprise_book.id, f"surp_{surprise_book.id}")


# -----------------------------------------------------------------------------
# 10. Page: My Reading Shelves
# -----------------------------------------------------------------------------
elif menu == "📖 My Reading Shelves":
    st.markdown("## 📖 My Atelier Reading Shelves")

    if not st.session_state.logged_in:
        st.warning("Please sign in or choose a reader profile in the sidebar to view and organize your reading shelves.")
    else:
        with flask_app.app_context():
            from app.services.reading_service import ReadingService
            from app.models.reading import ReadingRecord
            from app.models.book import Book

            user_id = st.session_state.user_id
            shelf_tabs = st.tabs(["⏳ Currently Reading", "📚 Want to Read", "✅ Completed"])

            shelf_keys = [("currently_reading", shelf_tabs[0]), ("want_to_read", shelf_tabs[1]), ("completed", shelf_tabs[2])]

            for status, tab in shelf_keys:
                with tab:
                    records = ReadingService.get_user_shelf(user_id=user_id, status=status)
                    if not records:
                        st.info(f"Your '{status.replace('_', ' ').title()}' shelf is currently empty.")
                    else:
                        for rec in records:
                            book = rec.book
                            st.markdown(f"""
                            <div class="book-card">
                                <h3 style="margin: 0;">{html.escape(book.title)}</h3>
                                <div style="color: #6b7280; font-style: italic;">by {html.escape(book.author)}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            col_c, col_info = st.columns([1, 3])
                            with col_c:
                                render_book_cover(book)
                            with col_info:
                                total_p = rec.total_pages or book.page_count or 100
                                current_p = rec.pages_read or 0
                                progress_pct = min(1.0, current_p / total_p) if total_p > 0 else 0.0

                                st.write(f"**Progress:** {current_p} / {total_p} pages ({int(progress_pct * 100)}%)")
                                st.progress(progress_pct)

                                # Update progress form
                                with st.expander("Update Reading Progress"):
                                    new_page = st.number_input(
                                        "Pages Read",
                                        min_value=0,
                                        max_value=total_p,
                                        value=current_p,
                                        key=f"p_{rec.id}"
                                    )
                                    if st.button("Save Progress", key=f"btn_p_{rec.id}"):
                                        ReadingService.update_progress(user_id=user_id, book_id=book.id, pages_read=new_page)
                                        st.toast("Progress updated!")
                                        st.rerun()

                                # Move shelf / delete
                                c_m1, c_m2 = st.columns(2)
                                with c_m1:
                                    target_shelf = st.selectbox(
                                        "Move to Shelf:",
                                        ["want_to_read", "currently_reading", "completed"],
                                        index=["want_to_read", "currently_reading", "completed"].index(status),
                                        key=f"mv_{rec.id}"
                                    )
                                    if target_shelf != status:
                                        if st.button("Move", key=f"btn_mv_{rec.id}"):
                                            ReadingService.set_shelf_status(user_id=user_id, book_id=book.id, status=target_shelf)
                                            st.toast(f"Moved to {target_shelf.replace('_', ' ').title()}!")
                                            st.rerun()
                                with c_m2:
                                    if st.button("🗑️ Remove from Shelf", key=f"rm_{rec.id}"):
                                        ReadingService.remove_from_shelf(user_id=user_id, book_id=book.id)
                                        st.toast("Removed from shelf.")
                                        st.rerun()
                            st.markdown("---")


# -----------------------------------------------------------------------------
# 11. Page: Wishlist
# -----------------------------------------------------------------------------
elif menu == "🤍 Wishlist":
    st.markdown("## 🤍 Private Wishlist")
    st.write("Books you aspire to acquire or explore in future reading seasons.")

    if not st.session_state.logged_in:
        st.warning("Please sign in or select a reader profile in the sidebar to access your wishlist.")
    else:
        with flask_app.app_context():
            from app.models.wishlist import Wishlist
            from app.services.reading_service import ReadingService

            user_id = st.session_state.user_id
            items = Wishlist.query.filter_by(user_id=user_id).order_by(Wishlist.added_at.desc()).all()

            if not items:
                st.info("Your wishlist is empty. Add volumes by browsing the Catalogue or Recommendations.")
            else:
                for item in items:
                    book = item.book
                    col_w1, col_w2 = st.columns([1, 3])
                    with col_w1:
                        render_book_cover(book)
                    with col_w2:
                        st.markdown(f"### {book.title}")
                        st.write(f"by *{book.author}* &nbsp;|&nbsp; ⭐ {book.rating:.1f}")
                        st.write(book.description)
                        st.caption(f"Added on: {item.added_at.strftime('%B %d, %Y') if item.added_at else 'Recent'}")

                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("📖 Move to Want to Read", key=f"w_mv_{book.id}"):
                                ReadingService.set_shelf_status(user_id=user_id, book_id=book.id, status="want_to_read")
                                remove_from_wishlist(user_id=user_id, book_id=book.id)
                                st.toast("Moved to 'Want to Read'!")
                                st.rerun()
                        with col_btn2:
                            if st.button("🗑️ Remove from Wishlist", key=f"w_del_{book.id}"):
                                remove_from_wishlist(user_id=user_id, book_id=book.id)
                                st.toast("Removed from Wishlist.")
                                st.rerun()
                    st.markdown("---")


# -----------------------------------------------------------------------------
# 12. Page: Reading Analytics & Goals
# -----------------------------------------------------------------------------
elif menu == "📊 Reading Analytics & Goals":
    st.markdown("## 📊 Reading Habits & Atelier Analytics")

    if not st.session_state.logged_in:
        st.warning("Please sign in or select a reader profile in the sidebar to view your analytics.")
    else:
        with flask_app.app_context():
            from app.services.statistics_service import StatisticsService
            from app.models.reading import ReadingRecord
            from app.models.goal import ReadingGoal
            from app.models.activity import ReadingActivity

            user_id = st.session_state.user_id
            streaks = StatisticsService.get_user_streaks(user_id)
            current_year = datetime.now(timezone.utc).year
            goal = ReadingGoal.query.filter_by(user_id=user_id, goal_year=current_year).first()

            completed_books_count = ReadingRecord.query.filter_by(user_id=user_id, status='completed').count()
            target_books = goal.target_books if goal else 12

            # Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{streaks['current_streak']}</div>
                    <div class="stat-label">Current Streak (Days)</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{streaks['longest_streak']}</div>
                    <div class="stat-label">Longest Streak (Days)</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{completed_books_count}</div>
                    <div class="stat-label">Books Completed</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{target_books}</div>
                    <div class="stat-label">{current_year} Annual Goal</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"### 🎯 Annual Goal Progress ({current_year})")
            goal_pct = min(1.0, completed_books_count / target_books) if target_books > 0 else 0
            st.write(f"You have read **{completed_books_count}** of **{target_books}** books ({int(goal_pct * 100)}% achieved).")
            st.progress(goal_pct)

            with st.expander("Update Annual Reading Target"):
                new_target = st.number_input("Target Books for " + str(current_year), min_value=1, max_value=200, value=target_books)
                if st.button("Save Reading Target"):
                    if not goal:
                        goal = ReadingGoal(user_id=user_id, goal_year=current_year, target_books=new_target)
                        db.session.add(goal)
                    else:
                        goal.target_books = new_target
                    db.session.commit()
                    st.toast("Annual goal updated!")
                    st.rerun()

            # Genre distribution
            st.markdown("### 📚 Genre Distribution in Completed Books")
            completed_records = ReadingRecord.query.filter_by(user_id=user_id, status='completed').all()
            genre_counts = {}
            for r in completed_records:
                for g in r.book.genres_list:
                    genre_counts[g] = genre_counts.get(g, 0) + 1

            if genre_counts:
                st.bar_chart(genre_counts)
            else:
                st.info("Complete books on your shelves to populate your personal genre distribution graph.")


# -----------------------------------------------------------------------------
# 13. Page: Reader Preferences
# -----------------------------------------------------------------------------
elif menu == "⚙️ Reader Preferences":
    st.markdown("## ⚙️ Reader Preferences & Taste Profile")
    st.write("Tailor your reading companion. These preferences directly power the 100-point explainable recommendation algorithm.")

    if not st.session_state.logged_in:
        st.warning("Please sign in or select a reader profile in the sidebar to configure preferences.")
    else:
        with flask_app.app_context():
            from app.models.user import User
            from app.models.preference import UserPreference
            from app.forms import ALL_GENRES

            user = db.session.get(User, st.session_state.user_id)
            pref = user.preference

            current_genres = pref.preferred_genres if pref and pref.preferred_genres else ["Fiction", "Philosophy"]
            current_languages = pref.preferred_languages if pref and pref.preferred_languages else ["English"]
            current_age = pref.age_preference if pref and pref.age_preference else "Adult"
            current_duration = pref.preferred_duration if pref and pref.preferred_duration else 30
            current_keywords = ", ".join(pref.interest_keywords) if pref and pref.interest_keywords else "wisdom, books, ideas"

            with st.form("pref_form"):
                new_genres = st.multiselect("Preferred Literary Genres", ALL_GENRES, default=[g for g in current_genres if g in ALL_GENRES])
                new_languages = st.multiselect("Reading Languages", ["English", "French", "Spanish", "German", "Latin", "Ancient Greek"], default=current_languages)
                new_age = st.selectbox("Age Category Suitability", ["All Ages", "Young Adult", "Adult", "Mature"], index=["All Ages", "Young Adult", "Adult", "Mature"].index(current_age))
                new_duration = st.slider("Preferred Session Duration (minutes)", 10, 120, current_duration, 5)
                new_keywords_str = st.text_input("Interest Keywords (comma-separated)", value=current_keywords)

                submitted = st.form_submit_button("Save Atelier Preferences", type="primary")
                if submitted:
                    keywords_list = [k.strip() for k in new_keywords_str.split(",") if k.strip()]
                    if not pref:
                        pref = UserPreference(
                            user_id=user.id,
                            preferred_genres=new_genres,
                            preferred_languages=new_languages,
                            age_preference=new_age,
                            preferred_duration=new_duration,
                            interest_keywords=keywords_list,
                            onboarding_completed=True
                        )
                        db.session.add(pref)
                    else:
                        pref.preferred_genres = new_genres
                        pref.preferred_languages = new_languages
                        pref.age_preference = new_age
                        pref.preferred_duration = new_duration
                        pref.interest_keywords = keywords_list
                        pref.onboarding_completed = True
                    db.session.commit()
                    st.success("Preferences updated successfully! Your recommendations will now reflect these preferences.")
                    st.rerun()
