from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Dependency function that provides a SQLAlchemy database session.

    Yields:
        Session: A SQLAlchemy session object.

    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
