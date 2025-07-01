from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL - using environment variables for flexibility
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/notepad_db"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()