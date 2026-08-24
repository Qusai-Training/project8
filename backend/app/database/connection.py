from sqlalchemy import create_engine
from app.config import settings

# Create engine for PostgreSQL connection using Core
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

def get_db_connection():
    """Context manager / dependency to acquire a raw SQLAlchemy Core connection."""
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()