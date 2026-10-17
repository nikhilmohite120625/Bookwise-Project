import pytest
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.preference import UserPreference
from app.models.book import Book
from seeds.sample_books import SAMPLE_BOOKS


@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application with in-memory SQLite."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Function-level database fixture with clean transaction rollback/reset."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app, db):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def sample_books(db):
    """Inserts a subset of sample books for testing."""
    books = []
    for b_data in SAMPLE_BOOKS[:10]:
        book = Book(**b_data)
        db.session.add(book)
        books.append(book)
    db.session.commit()
    return books


@pytest.fixture
def test_user(db):
    """Creates a standard test reader user."""
    user = User(
        name="Arthur Reader",
        email="arthur@example.com",
        role="user"
    )
    user.set_password("SecurePassword2026!")
    db.session.add(user)
    db.session.flush()

    pref = UserPreference(
        user_id=user.id,
        preferred_genres=["Fantasy", "Philosophy"],
        preferred_languages=["English"],
        age_preference="Adult",
        preferred_duration=30,
        interest_keywords=["magic", "stoicism", "resilience"],
        onboarding_completed=True,
        theme_preference="light"
    )
    db.session.add(pref)
    db.session.commit()
    return user


@pytest.fixture
def admin_user(db):
    """Creates an administrative curator user."""
    admin = User(
        name="Curator Administrator",
        email="admin@example.com",
        role="admin"
    )
    admin.set_password("AdminSecurePassword2026!")
    db.session.add(admin)
    db.session.flush()

    pref = UserPreference(
        user_id=admin.id,
        preferred_genres=["Philosophy", "History"],
        preferred_languages=["English"],
        age_preference="Adult",
        preferred_duration=30,
        interest_keywords=["wisdom"],
        onboarding_completed=True,
        theme_preference="dark"
    )
    db.session.add(pref)
    db.session.commit()
    return admin
