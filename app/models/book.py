import html
from datetime import datetime, timezone
from app.extensions import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    genres = db.Column(db.JSON, default=list, nullable=False)
    language = db.Column(db.String(64), default='English', nullable=False)
    publication_year = db.Column(db.Integer, nullable=True, index=True)
    age_suitability = db.Column(db.String(32), default='Adult', nullable=False)  # All Ages, Young Adult, Adult, Mature
    estimated_duration = db.Column(db.Integer, nullable=True)  # in minutes
    keywords = db.Column(db.JSON, default=list, nullable=False)
    rating = db.Column(db.Float, default=4.2, nullable=True)  # Sample catalogue rating
    isbn = db.Column(db.String(32), nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    reading_records = db.relationship('ReadingRecord', back_populates='book', cascade='all, delete-orphan', lazy='dynamic')
    wishlist_items = db.relationship('Wishlist', back_populates='book', cascade='all, delete-orphan', lazy='dynamic')
    reading_sessions = db.relationship('ReadingSession', back_populates='book', lazy='dynamic')
    journal_entries = db.relationship('ReadingJournalEntry', back_populates='book', lazy='dynamic')
    collection_items = db.relationship('CollectionItem', back_populates='book', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def genres_list(self) -> list:
        if isinstance(self.genres, list):
            return self.genres
        return []

    @property
    def keywords_list(self) -> list:
        if isinstance(self.keywords, list):
            return self.keywords
        return []

    @property
    def primary_genre(self) -> str:
        genres = self.genres_list
        return genres[0] if genres else 'Uncategorized'

    def get_fallback_svg(self) -> str:
        """Generates an elegant inline SVG placeholder cover with The Reading Atelier aesthetics."""
        safe_title = html.escape((self.title or 'BookWise Volume')[:40])
        safe_author = html.escape((self.author or 'Unknown Author')[:32])
        safe_genre = html.escape((self.primary_genre or 'Literature').upper())
        # Deterministic hue shift based on title hash
        hue = (abs(hash(self.title or 'book')) % 40) + 145  # Rich forest/emerald hues
        return f"""data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 450' width='100%' height='100%'>
          <defs>
            <linearGradient id='grad' x1='0%' y1='0%' x2='100%' y2='100%'>
              <stop offset='0%' stop-color='hsl({hue}, 40%, 18%)' />
              <stop offset='100%' stop-color='hsl({hue + 15}, 45%, 11%)' />
            </linearGradient>
            <pattern id='cloth' width='20' height='20' patternUnits='userSpaceOnUse'>
              <path d='M0 10h20M10 0v20' stroke='rgba(255,255,255,0.02)' stroke-width='1'/>
            </pattern>
          </defs>
          <rect width='300' height='450' fill='url(%23grad)' />
          <rect width='300' height='450' fill='url(%23cloth)' />
          <rect x='12' y='12' width='276' height='426' fill='none' stroke='%23c5a059' stroke-width='1.5' stroke-opacity='0.6' rx='4'/>
          <rect x='18' y='18' width='264' height='414' fill='none' stroke='%23c5a059' stroke-width='0.75' stroke-dasharray='4,3' stroke-opacity='0.4' rx='3'/>
          <path d='M20 0v450' stroke='rgba(0,0,0,0.35)' stroke-width='14'/>
          <path d='M27 0v450' stroke='%23c5a059' stroke-width='1' stroke-opacity='0.3'/>
          <text x='150' y='65' font-family='serif' font-size='10' font-weight='600' letter-spacing='3' fill='%23c5a059' text-anchor='middle'>{safe_genre}</text>
          <line x1='110' y1='75' x2='190' y2='75' stroke='%23c5a059' stroke-width='1' stroke-opacity='0.4'/>
          <foreignObject x='35' y='140' width='230' height='160'>
            <div xmlns='http://www.w3.org/1999/xhtml' style='color:%23fbf8f3; font-family:serif; font-size:22px; line-height:1.25; text-align:center; font-weight:700; word-break:break-word; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>
              {safe_title}
            </div>
          </foreignObject>
          <line x1='125' y1='335' x2='175' y2='335' stroke='%23c5a059' stroke-width='1' stroke-opacity='0.5'/>
          <text x='150' y='365' font-family='sans-serif' font-size='13' font-style='italic' fill='%23e0d7c7' text-anchor='middle'>{safe_author}</text>
          <text x='150' y='410' font-family='sans-serif' font-size='9' letter-spacing='1.5' fill='%23c5a059' opacity='0.7' text-anchor='middle'>BOOKWISE ATELIER</text>
        </svg>"""

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'genres': self.genres_list,
            'language': self.language,
            'publication_year': self.publication_year,
            'age_suitability': self.age_suitability,
            'estimated_duration': self.estimated_duration,
            'keywords': self.keywords_list,
            'rating': self.rating,
            'isbn': self.isbn,
            'cover_url': self.cover_url or self.get_fallback_svg(),
            'page_count': self.page_count
        }

    def __repr__(self):
        return f'<Book {self.id}: "{self.title}" by {self.author}>'
