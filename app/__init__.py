import os
from flask import Flask, render_template
from app.config import config_by_name
from app.extensions import db, migrate, login_manager, csrf, limiter
from app.models.user import User


def create_app(config_name=None):
    """Application factory for BookWise Atelier."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    # Production invariant check: never silently fall back to ephemeral SQLite in production
    if config_name == 'production':
        if not os.environ.get('DATABASE_URL'):
            raise ValueError(
                "DATABASE_URL environment variable must be configured in production (MySQL 8 or PostgreSQL). "
                "Ephemeral SQLite fallback is disallowed in production."
            )
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production.")

    config_class = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Configure user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.discover import discover_bp
    from app.routes.reading import reading_bp
    from app.routes.timer import timer_bp
    from app.routes.calendar import calendar_bp
    from app.routes.journal import journal_bp
    from app.routes.collections import collections_bp
    from app.routes.statistics import statistics_bp
    from app.routes.assistant import assistant_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(discover_bp)
    app.register_blueprint(reading_bp)
    app.register_blueprint(timer_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def access_forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return render_template('errors/429.html', error_description=e.description), 429

    # Context processors for global template availability
    @app.context_processor
    def inject_globals():
        from app.forms import ALL_GENRES
        from datetime import datetime, timezone
        return {
            'GLOBAL_GENRES': ALL_GENRES,
            'CURRENT_YEAR': datetime.now(timezone.utc).year
        }

    # Custom CLI commands
    @app.cli.command('seed-db')
    def seed_db_command():
        """CLI command to seed the database with sample catalogue books and admin."""
        from seeds.sample_books import seed_database
        count = seed_database(db)
        print(f"Successfully populated database with {count} sample books and admin curator.")

    return app
