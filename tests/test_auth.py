import pytest
from app.models.user import User
from app.models.reading import ReadingRecord
from app.models.book import Book


def test_registration_and_hashing(client, db):
    response = client.post('/register', data={
        'name': 'New Reader',
        'email': 'newreader@example.com',
        'password': 'StrongPassword123!',
        'confirm_password': 'StrongPassword123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(email='newreader@example.com').first()
    assert user is not None
    assert user.name == 'New Reader'
    assert user.password_hash != 'StrongPassword123!'
    assert user.check_password('StrongPassword123!')
    assert user.preference is not None


def test_duplicate_email_rejected(client, db, test_user):
    response = client.post('/register', data={
        'name': 'Imposter',
        'email': test_user.email,  # duplicate
        'password': 'StrongPassword123!',
        'confirm_password': 'StrongPassword123!'
    })
    # Should not register and display validation error
    assert b'already exists' in response.data or response.status_code != 302


def test_login_and_logout(client, db, test_user):
    # Valid login
    resp = client.post('/login', data={
        'email': test_user.email,
        'password': 'SecurePassword2026!'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Welcome back' in resp.data or b'My Books' in resp.data

    # Logout
    resp_logout = client.get('/logout', follow_redirects=True)
    assert resp_logout.status_code == 200
    assert b'signed out' in resp_logout.data


def test_admin_authorization(client, db, test_user, admin_user):
    # Standard user blocked from admin
    client.post('/login', data={'email': test_user.email, 'password': 'SecurePassword2026!'}, follow_redirects=True)
    resp = client.get('/admin/', follow_redirects=False)
    assert resp.status_code in [403, 302]

    client.get('/logout')

    # Admin user allowed into admin
    client.post('/login', data={'email': admin_user.email, 'password': 'AdminSecurePassword2026!'}, follow_redirects=True)
    resp_admin = client.get('/admin/', follow_redirects=True)
    assert resp_admin.status_code == 200
    assert b'Catalogue Administration' in resp_admin.data or b'Curator Console' in resp_admin.data


def test_account_deletion_cascade(client, db, test_user):
    # Add a book and reading record for test_user
    book = Book(title="Cascade Book", author="Author", genres=["Fiction"], language="English")
    db.session.add(book)
    db.session.commit()

    rec = ReadingRecord(user_id=test_user.id, book_id=book.id, status='want_to_read')
    db.session.add(rec)
    db.session.commit()

    # Login and delete account
    client.post('/login', data={'email': test_user.email, 'password': 'SecurePassword2026!'}, follow_redirects=True)
    resp = client.post('/profile/delete-account', data={
        'confirm_email': test_user.email,
        'password': 'SecurePassword2026!'
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert User.query.filter_by(id=test_user.id).first() is None
    # Cascade check: reading records deleted
    assert ReadingRecord.query.filter_by(user_id=test_user.id).first() is None
