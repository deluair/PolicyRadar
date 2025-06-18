"""
Base SQLAlchemy model for PolicyRadar.
"""
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Column, Integer, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel


class Base:
    """Base class for all models."""
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    metadata = Column(Text, nullable=True)  # JSON string for additional data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update model from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def get_by_id(cls, db: Session, id: int):
        """Get model by ID."""
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100):
        """Get all models with pagination."""
        return db.query(cls).offset(skip).limit(limit).all()


# Create declarative base
Base = declarative_base(cls=Base)


class BaseSchema(BaseModel):
    """Base Pydantic schema."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 