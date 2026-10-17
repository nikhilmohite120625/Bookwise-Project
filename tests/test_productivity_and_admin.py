import pytest
from app.models.book import Book
from app.models.journal import ReadingJournalEntry
from app.models.collection import PersonalCollection, CollectionItem
from app.services.journal_service import JournalService
from app.services.collection_service import CollectionService
from app.services.statistics_service import StatisticsService


def test_journal_service_crud(db, test_user):
    # Create
    entry = JournalService.create_entry(
        user_id=test_user.id,
        title="Stoic Morning Thoughts",
        content="Focus exclusively on what is within your voluntary control."
    )
    assert entry.id is not None
    assert entry.title == "Stoic Morning Thoughts"

    # Read
    entries = JournalService.get_user_entries(user_id=test_user.id)
    assert len(entries) == 1
    assert entries[0].id == entry.id

    # Update
    updated = JournalService.update_entry(
        entry_id=entry.id,
        user_id=test_user.id,
        title="Updated Stoic Thoughts",
        content="Amor fati."
    )
    assert updated.title == "Updated Stoic Thoughts"

    # Delete
    deleted = JournalService.delete_entry(entry_id=entry.id, user_id=test_user.id)
    assert deleted is True
    assert len(JournalService.get_user_entries(user_id=test_user.id)) == 0


def test_collection_service_crud(db, test_user):
    b1 = Book(title="Book 1", author="A", genres=["Philosophy"], language="English")
    b2 = Book(title="Book 2", author="B", genres=["History"], language="English")
    db.session.add_all([b1, b2])
    db.session.commit()

    # Create collection
    coll = CollectionService.create_collection(
        user_id=test_user.id,
        name="Essential Philosophy",
        description="Core foundational works."
    )
    assert coll.id is not None

    # Add items
    item1 = CollectionService.add_book_to_collection(coll.id, test_user.id, b1.id)
    assert item1.position == 1
    item2 = CollectionService.add_book_to_collection(coll.id, test_user.id, b2.id)
    assert item2.position == 2

    # Prevent duplicate
    dup = CollectionService.add_book_to_collection(coll.id, test_user.id, b1.id)
    assert dup.id == item1.id
    assert coll.items.count() == 2

    # Remove book
    CollectionService.remove_book_from_collection(coll.id, test_user.id, b1.id)
    assert coll.items.count() == 1

    # Delete collection
    deleted = CollectionService.delete_collection(coll.id, test_user.id)
    assert deleted is True
    assert PersonalCollection.query.filter_by(id=coll.id).first() is None


def test_statistics_calculations(db, test_user):
    summary = StatisticsService.get_dashboard_summary(test_user.id)
    assert 'streaks' in summary
    assert 'goals' in summary
    assert 'shelf_counts' in summary
    assert summary['shelf_counts']['want_to_read'] == 0


def test_admin_book_management(client, db, admin_user):
    client.post('/login', data={'email': admin_user.email, 'password': 'AdminSecurePassword2026!'}, follow_redirects=True)

    # Add book
    resp = client.post('/admin/books/add', data={
        'title': 'The Republic',
        'author': 'Plato',
        'description': 'Dialogues on justice and the ideal state.',
        'genres': 'Philosophy, Classics',
        'language': 'English',
        'publication_year': 375,
        'age_suitability': 'Adult',
        'estimated_duration': 40,
        'keywords': 'justice, state, ethics',
        'rating': 4.7,
        'page_count': 416
    }, follow_redirects=True)
    assert resp.status_code == 200

    book = Book.query.filter_by(title='The Republic').first()
    assert book is not None
    assert book.author == 'Plato'
    assert 'Philosophy' in book.genres_list

    # Edit book
    resp_edit = client.post(f'/admin/books/{book.id}/edit', data={
        'title': 'The Republic (Second Edition)',
        'author': 'Plato',
        'genres': 'Philosophy, Political Theory',
        'language': 'English',
        'age_suitability': 'Adult',
        'rating': 4.8
    }, follow_redirects=True)
    assert resp_edit.status_code == 200
    assert Book.query.get(book.id).title == 'The Republic (Second Edition)'

    # Delete book
    resp_delete = client.post(f'/admin/books/{book.id}/delete', follow_redirects=True)
    assert resp_delete.status_code == 200
    assert Book.query.filter_by(title='The Republic (Second Edition)').first() is None
