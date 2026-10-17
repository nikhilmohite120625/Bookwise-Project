import pytest
from app.models.book import Book


def test_api_endpoints(client, db, test_user):
    b = Book(title="API Test Book", author="Coder", genres=["Technology"], language="English", estimated_duration=25)
    db.session.add(b)
    db.session.commit()

    # Search endpoint (public)
    resp = client.get('/api/search?q=API')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['results']) >= 1
    assert data['results'][0]['title'] == "API Test Book"

    # Surprise Me endpoint
    resp_surprise = client.get('/api/surprise-me')
    assert resp_surprise.status_code == 200
    assert resp_surprise.get_json()['status'] == 'success'

    # Authenticated endpoints
    client.post('/login', data={'email': test_user.email, 'password': 'SecurePassword2026!'})
    
    # Recommendations endpoint
    resp_recs = client.get('/api/recommendations')
    assert resp_recs.status_code == 200
    assert resp_recs.get_json()['status'] == 'success'
