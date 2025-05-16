# db.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(str(os.getenv("DB_PASSWORD")))  # URL encode the password
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Get a new SQLAlchemy session."""
    return SessionLocal()

def fetchall(query: str, params: dict = None) -> list[dict]:
    """Run a SELECT query and return all results as a list of dicts."""
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return [dict(row) for row in result]

def execute(query: str, params: dict = None) -> None:
    """Run an INSERT/UPDATE/DELETE query."""
    with engine.connect() as conn:
        conn.execute(text(query), params or {})
        conn.commit()

# Optional: Add a test function to verify connection
def test_connection() -> bool:
    """Test database connection."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    # Test the connection when running this file directly
    if test_connection():
        print("Database connection successful!")
    else:
        print("Failed to connect to database!")