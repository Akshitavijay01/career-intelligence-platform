from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLite configuration
# For SQLite, we need to handle some differences from PostgreSQL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Configure engine for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=settings.DEBUG
)

# For PostgreSQL, use this instead (if needed for production):
# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,
#     echo=settings.DEBUG
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)