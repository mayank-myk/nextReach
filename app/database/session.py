from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.utils.config import get_config

MAX_POOL_CONN = 5
MAX_OVERFLOW = 10
DATABASE_URL = get_config("PROD_OTHERS_DB_WRITER_URL")

# Create SQLAlchemy Engine and Session
engine = create_engine(DATABASE_URL, pool_size=MAX_POOL_CONN, max_overflow=10)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def get_db_session():
    """Dependency to inject a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseSessionManager:
    """Abstraction for SQLAlchemy session management."""

    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(db_url, pool_size=10,  # Increase pool size as needed
                                    max_overflow=20,  # Number of connections to allow beyond pool_size
                                    pool_timeout=30,  # Timeout for getting a connection from the pool
                                    pool_recycle=1800)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        """Dependency to provide a session for each request."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
