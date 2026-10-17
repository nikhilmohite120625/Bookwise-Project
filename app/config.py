import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class BaseConfig:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bookwise-atelier-secret-key-default-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cookie & Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    
    # CSRF & Rate Limiting
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    RATELIMIT_DEFAULT = "200 per day; 60 per hour"
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    RATELIMIT_HEADERS_ENABLED = True

    # Database resolution: MySQL primary with SQLite local fallback
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.strip():
        # Handle dialect normalization if user passes mysql:// instead of mysql+pymysql://
        if db_url.startswith('mysql://'):
            db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = db_url
        IS_SQLITE = False
    else:
        # SQLite local development fallback
        instance_dir = BASE_DIR / 'instance'
        instance_dir.mkdir(exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{instance_dir / 'bookwise.db'}"
        IS_SQLITE = True


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    DEBUG = True
    ENV = 'development'
    SESSION_COOKIE_SECURE = False


class TestingConfig(BaseConfig):
    """Testing environment configuration using isolated in-memory SQLite."""
    TESTING = True
    DEBUG = False
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SESSION_COOKIE_SECURE = False
    IS_SQLITE = True


class ProductionConfig(BaseConfig):
    """Production configuration requiring robust secrets and database."""
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
    
    def __init__(self):
        super().__init__()
        # Validate production invariants: do not silently run in production with default secrets or missing database
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production.")
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL environment variable must be configured in production (MySQL 8). Ephemeral SQLite fallback is disallowed in production.")


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
