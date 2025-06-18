#!/usr/bin/env python3
"""
Script to set up the database for PolicyRadar.
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, check_database_health
from data.models.base import Base
from loguru import logger


def main():
    """Main function to set up the database."""
    logger.info("Setting up PolicyRadar database...")
    
    try:
        # Check database connectivity
        if not check_database_health():
            logger.error("Database connection failed. Please check your database configuration.")
            return
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database setup completed successfully!")
        logger.info("All tables have been created.")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


if __name__ == "__main__":
    main() 