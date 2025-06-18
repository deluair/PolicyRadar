"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import redis
from loguru import logger

from config.settings import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Redis connection
redis_client = redis.from_url(settings.redis_url)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """
    Get Redis client.
    
    Returns:
        Redis: Redis client instance
    """
    return redis_client


# Database health check
def check_database_health() -> bool:
    """
    Check database connectivity.
    
    Returns:
        bool: True if database is healthy, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Redis health check
def check_redis_health() -> bool:
    """
    Check Redis connectivity.
    
    Returns:
        bool: True if Redis is healthy, False otherwise
    """
    try:
        redis_client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False 