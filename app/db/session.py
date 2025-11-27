"""
Optimized database session management for local Docker PostgreSQL.
"""
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create engine with local PostgreSQL optimizations
try:
    logger.info(f"Creating database engine for local PostgreSQL: {settings.DATABASE_URL}")
    engine = create_engine(
        settings.DATABASE_URL,
        # Optimized for local Docker PostgreSQL
        pool_size=5,            # Smaller pool for local development
        max_overflow=10,        # Reasonable overflow
        pool_timeout=10,        # Quick timeout for local
        pool_recycle=1800,      # 30 minute recycle for local
        pool_pre_ping=True,     # Validate connections
        
        # Local connection optimization
        connect_args={
            "connect_timeout": 5,
            "application_name": "regel_backend_local",
        },
        
        # Performance settings
        echo=False,             # No SQL logging for speed
    )
    
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine,
        expire_on_commit=False  # Keep objects accessible after commit
    )
    
    logger.info("Local database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise


def get_db():
    """Production database session with connection reuse."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()