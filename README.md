# BookWise — The Reading Atelier
> **Tagline:** *Find Your Next Favourite Book.*

BookWise is a production-oriented, responsive, full-stack web application designed as a digital reading companion and explainable book recommendation platform. Built around **"The Reading Atelier"** visual identity (warm ivory backgrounds, deep forest-green, midnight-navy, antique-gold accents, and classical serif typography), BookWise prioritizes intellectual depth, habit tracking, and explainable discovery.

Unlike generic platforms relying on opaque black-box APIs, BookWise features a **100% deterministic, transparent 5-dimension recommendation engine** running entirely locally without external AI API dependencies.

---

## 🌟 Key Features

### 1. Explainable 100-Point Recommendation Engine
Evaluates every candidate book against five dimensions:
- **Genre Compatibility (Max 40 Pts):** Awarded when book genres intersect with user preferred genres.
- **Language Compatibility (Max 20 Pts):** Awarded when book language matches reader preferred languages.
- **Age Suitability (Max 15 Pts):** Strict hierarchy validation (*All Ages &rarr; Young Adult &rarr; Adult &rarr; Mature*). Never awards positive points for unsuitable books.
- **Reading Duration Pace (Max 15 Pts):** Proximity formula:
  $$\text{Duration Score} = 15 \times \max\left(0, 1 - \frac{|B - T|}{T}\right)$$
  where $T$ is user target duration in minutes and $B$ is estimated book session duration.
- **Interest Keyword Affinity (Max 10 Pts):** Normalized token-boundary matching across searchable book text:
  $$\text{Interest Score} = 10 \times \frac{\text{matched unique user keywords}}{\text{total unique user keywords}}$$
- **Auditable Tie-Breaking:**
  1. Total Compatibility Score $\downarrow$
  2. Catalogue Community Rating $\downarrow$
  3. Publication Year $\downarrow$
  4. Book Title (Case-Insensitive) $\uparrow$
  5. Book ID $\uparrow$

Every recommendation displays an expandable **"Why this book?"** breakdown with individual dimension bars and specific rationale statements.

### 2. Reading Shelves ("My Books")
- **Want to Read:** Save prospective books and organize a custom **Priority Queue**.
- **Currently Reading:** Live progress bars, page tracking ($0 \le \text{pages} \le \text{total}$), and private notes.
- **Completed:** Automatic completion date stamping, ratings (1–5 stars), and celebration logs.
- Safe transitions between shelves updating existing records (strict unique constraint on `(user_id, book_id)`).

### 3. Reading Productivity Tools
- **Live Reading Stopwatch / Timer (`/timer`):** Minimalist dial with start/pause/reset, focus mode, and session saving with **idempotency token deduplication**.
- **Habit Streaks & Interactive Calendar (`/calendar`):** Real-time daily streak calculation, all-time record, and a monthly heatmap tracking minutes, pages, and books read.
- **Private Literary Journal (`/journal`):** Private reflections, chapter takeaways, and favorite quotes linked to specific books.
- **Personal Collections (`/collections`):** Curate custom bundles (e.g. *"Stoic Philosophy Masterclass"*, *"Sci-Fi Essentials"*).
- **Reading Goals & Analytics (`/statistics`):** Annual target pacing and Chart.js visualizations for monthly velocity and genre distribution.

### 4. Advanced Discovery Hub
- **Mood-Based Discovery:** Select moods (*Comforting, Adventurous, Thought-provoking, Mysterious, Inspiring, Educational, Lighthearted, Romantic, Suspenseful*) mapped deterministically to genre and keyword rules.
- **Reading-Time Finder:** Filter books by 10, 20, 30, 45, or 60-minute windows.
- **Surprise Me:** Serendipitous book selection respecting user age suitability and unread status.
- **Side-by-Side Book Comparison (`/compare`):** Matrix comparison for 2–3 books showing metadata, ratings, and personalized compatibility scores.
- **Similar Books:** Deterministic attribute matching on shared genres, themes, and author.

### 5. Rule-Based Literary Assistant (`/assistant`)
Interactive conversational guide answering queries like:
- *"I have 30 minutes to read"*
- *"Suggest a mysterious novel"*
- *"How is my reading goal doing?"*
- *"What should I read next?"*

### 6. Administration Console (`/admin`)
- Role-protected (`role == 'admin'`) curator dashboard.
- Full CRUD management of catalogue books with server-side CSRF validation.
- One-click sample catalogue seeding tool.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12+, Flask 3.0, Flask-Login, Flask-WTF, Flask-Limiter, Werkzeug |
| **Database & ORM** | SQLAlchemy 2.0, Flask-SQLAlchemy, Flask-Migrate, Alembic, MySQL 8 (Primary) / SQLite (Zero-config fallback) |
| **Frontend** | Semantic HTML5, CSS3 Custom Properties, Vanilla Modular JavaScript, Chart.js, Google Fonts (*Playfair Display*, *Cinzel*, *Inter*) |
| **Testing** | pytest, pytest-flask, in-memory SQLite fixtures |
| **Deployment** | Gunicorn WSGI, Render `render.yaml`, `Procfile` |

---

## 📂 Project Structure

```
BookWise/
├── app/
│   ├── __init__.py               # Application factory, extensions, error handlers
│   ├── config.py                 # Development, Testing, Production configurations
│   ├── extensions.py             # db, migrate, login_manager, csrf, limiter
│   ├── forms.py                  # WTForms with CSRF & server-side validation
│   ├── models/                   # Relational SQLAlchemy models
│   │   ├── user.py               # User authentication & roles
│   │   ├── preference.py         # Reader preferences & calibration
│   │   ├── book.py               # Catalogue books & SVG cover generator
│   │   ├── reading.py            # ReadingRecord shelves (Want, Reading, Completed)
│   │   ├── wishlist.py           # Wishlist items
│   │   ├── goal.py               # Annual reading goals
│   │   ├── session.py            # Reading sessions with idempotency tokens
│   │   ├── journal.py            # Private reading journal entries
│   │   ├── collection.py         # Personal collections & items
│   │   └── activity.py           # Daily reading activity & streak data
│   ├── routes/                   # Modular blueprints
│   │   ├── main.py               # Landing page & health check
│   │   ├── auth.py               # Register, login, onboarding, profile, delete account
│   │   ├── books.py              # Catalogue browse, book detail, comparison
│   │   ├── recommendations.py    # Dedicated explainable recommendations feed
│   │   ├── discover.py           # Moods, reading-time finder, surprise me
│   │   ├── reading.py            # Shelves, progress logs, queue, wishlist
│   │   ├── timer.py              # Stopwatch companion & session logging
│   │   ├── calendar.py           # Reading calendar & streaks
│   │   ├── journal.py            # Private reflections
│   │   ├── collections.py        # Curated user collections
│   │   ├── statistics.py         # Analytics & Chart.js feeds
│   │   ├── assistant.py          # Rule-based conversational companion
│   │   ├── admin.py              # Protected catalogue administration
│   │   └── api.py                # REST endpoints
│   ├── services/                 # Pure domain business logic
│   │   ├── recommendation_service.py # 5-dimension deterministic scoring engine
│   │   ├── discovery_service.py  # Mood mapping, surprise me, similar books
│   │   ├── reading_service.py    # Shelf state transitions & activity logging
│   │   ├── session_service.py    # Stopwatch session recording & deduplication
│   │   ├── statistics_service.py # Streak math, monthly pacing, calendar heatmap
│   │   ├── journal_service.py    # Journal CRUD
│   │   ├── collection_service.py # Collection management
│   │   └── assistant_service.py  # Rule-based companion processor
│   ├── static/                   # Modular client assets
│   │   ├── css/                  # The Reading Atelier Design System
│   │   └── js/                   # Vanilla modular scripts (timer, charts, assistant)
│   └── templates/                # Jinja2 templates (responsive Atelier UI)
├── seeds/
│   └── sample_books.py           # 36 diverse seed books across 15 genres
├── tests/                        # 24 automated pytest tests
├── Procfile                      # Gunicorn command
├── render.yaml                   # Render deployment configuration
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── run.py                        # Application entry point
```

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- pip

### 1. Clone & Enter Project
```bash
git clone https://github.com/your-username/bookwise.git
cd bookwise
```

### 2. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
By default, `DATABASE_URL` is empty, which prompts BookWise to automatically fall back to zero-configuration local SQLite (`instance/bookwise.db`).

### 4. Run Application
```bash
py run.py
```
Visit `http://localhost:5000` in your browser.
On initial run, BookWise automatically initializes the database schema and seeds 36 sample books and an administrator account.

---

## 🔑 Administrator & Account Provisioning

BookWise follows zero-hardcoded-credentials security standards:
- **Reader Accounts**: Self-register via `/register` (passwords hashed using NIST/OWASP-approved `scrypt`).
- **Curator Admin Account**: Can be provisioned via:
  1. **Environment Variables**: Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in your `.env` or cloud dashboard. When initial database seeding runs, the admin account is securely created with a hashed password.
  2. **CLI Command**: Run the interactive or scripted CLI tool:
     ```bash
     flask create-admin --email admin@example.com --password YourSecurePassword123! --name "Atelier Curator"
     ```
- **Catalogue Seeding**: Populate or reset the sample book collection:
  ```bash
  flask seed-db
  ```

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
py -m pytest -v --tb=short
```

Test coverage includes:
- Recommendation scoring across all 5 dimensions (score boundaries, clamping, missing preferences).
- Deterministic multi-tier tie-breaking and eligibility exclusions.
- Authentication, scrypt password hashing, CSRF protection, and cascade account deletion.
- Role-based authorization for administrative endpoints.
- Reading shelf state transitions, page clamping, and completion date auto-fill.
- Reading timer idempotency deduplication and streak calculation.
- Mood-based discovery, reading-time finder, and rule-based assistant queries.
- REST API endpoint contracts.

---

## 🗄️ Database Strategy: MySQL 8 & SQLite Fallback

### Development (SQLite)
Zero setup required. If `DATABASE_URL` is omitted, `app/config.py` uses:
`sqlite:///instance/bookwise.db`.

### Production (MySQL 8)
Set `DATABASE_URL` in your environment:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/bookwise_db
```
*Note: In production (`FLASK_ENV=production`), silent fallback to SQLite is disallowed.*

### Migrations with Alembic / Flask-Migrate
Initialize and apply migrations when making schema changes:
```bash
flask db init
flask db migrate -m "Schema update"
flask db upgrade
```

---

## 🌐 Production Serving & Deployment

### Serving with Gunicorn
```bash
gunicorn run:app --bind 0.0.0.0:5000 --workers 4 --threads 2
```

### Render Deployment
BookWise includes `render.yaml` and `Procfile`. Push the repository to GitHub and connect to Render:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn run:app`
- **Health Check Path:** `/health`
- Connect a managed MySQL 8 database instance.

---

## 🛡️ Security Architecture
1. **Password Hashing:** Uses Werkzeug's secure hashing algorithms (`scrypt` / `pbkdf2:sha256`) with unique salts. Plaintext passwords are never stored.
2. **Session Security:** Cookies configured with `HttpOnly=True` and `SameSite=Lax`. Production mode enforces `Secure=True` under HTTPS.
3. **CSRF Protection:** Flask-WTF protects all form submissions and state-changing POST requests.
4. **Rate Limiting:** Flask-Limiter protects login endpoints against brute-force attacks.
5. **Data Isolation & Cascades:** All shelves, sessions, goals, journals, and collections enforce strict user ownership. Account deletion cascades cleanly across all associated data.
