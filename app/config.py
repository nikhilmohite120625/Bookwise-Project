import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def _resolve_database_uri():
    """Resolves database URI from DATABASE_URL or discrete DB credentials from environment."""
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url and raw_db_url.strip():
        db_url = raw_db_url.strip()
        # Handle dialect normalization:
        # 1. Render PostgreSQL provides postgres:// which SQLAlchemy 2.0 requires as postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        # 2. MySQL normalization to mysql+pymysql:// if mysql:// provided
        elif db_url.startswith('mysql://'):
            db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
        return db_url, False

    # Check for discrete database connection environment variables
    db_user = os.environ.get('DB_USER')
    db_name = os.environ.get('DB_NAME')
    if db_user and db_name:
        from urllib.parse import quote_plus
        db_pass = os.environ.get('DB_PASSWORD', '')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT')
        db_dialect = os.environ.get('DB_DIALECT', 'mysql+pymysql')
        
        encoded_pass = f":{quote_plus(db_pass)}" if db_pass else ""
        port_str = f":{db_port}" if db_port else ""
        return f"{db_dialect}://{quote_plus(db_user)}{encoded_pass}@{db_host}{port_str}/{db_name}", False

    # Local SQLite fallback for development
    instance_dir = BASE_DIR / 'instance'
    instance_dir.mkdir(exist_ok=True)
    return f"sqlite:///{instance_dir / 'bookwise.db'}", True


_db_uri, _is_sqlite = _resolve_database_uri()


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

    # Database resolution
    SQLALCHEMY_DATABASE_URI = _db_uri
    IS_SQLITE = _is_sqlite


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
    SECRET_KEY = os.environ.get('SECRET_KEY')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
