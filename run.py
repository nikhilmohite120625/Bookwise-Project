import os
from app import create_app
from app.extensions import db
from seeds.sample_books import seed_database

app = create_app(os.environ.get('FLASK_ENV', 'development'))

with app.app_context():
    # Automatically create tables for SQLite/dev convenience
    db.create_all()
    # If book catalogue is empty, seed initial books
    from app.models.book import Book
    if Book.query.count() == 0:
        seed_database(db)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
