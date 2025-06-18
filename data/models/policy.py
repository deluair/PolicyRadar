"""
Policy-related data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from .base import Base


class PolicyStatus(enum.Enum):
    """Policy status enumeration."""
    DRAFT = "draft"
    PROPOSED = "proposed"
    ENACTED = "enacted"
    IMPLEMENTED = "implemented"
    AMENDED = "amended"
    REPEALED = "repealed"
    EXPIRED = "expired"


class PolicyType(enum.Enum):
    """Policy type enumeration."""
    LEGISLATION = "legislation"
    REGULATION = "regulation"
    EXECUTIVE_ORDER = "executive_order"
    GUIDANCE = "guidance"
    STANDARD = "standard"
    AGREEMENT = "agreement"


class PolicyCategory(Base):
    """Policy category model."""
    __tablename__ = "policy_categories"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey("policy_categories.id"), nullable=True)
    
    # Relationships
    parent_category = relationship("PolicyCategory", remote_side="PolicyCategory.id")
    sub_categories = relationship("PolicyCategory")
    policies = relationship("Policy", back_populates="category")


class Policy(Base):
    """Policy model."""
    __tablename__ = "policies"
    
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    policy_number = Column(String(100), unique=True, nullable=False, index=True)
    jurisdiction = Column(String(10), nullable=False, index=True)
    policy_type = Column(Enum(PolicyType), nullable=False)
    status = Column(Enum(PolicyStatus), nullable=False, default=PolicyStatus.DRAFT)
    
    # Dates
    proposed_date = Column(DateTime, nullable=True)
    enacted_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    
    # Regulatory body
    regulatory_body = Column(String(200), nullable=True)
    authority = Column(String(200), nullable=True)
    
    # Content and metadata
    content_summary = Column(Text, nullable=True)
    full_text_url = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)
    
    # Impact assessment
    estimated_impact = Column(Float, nullable=True)  # In millions USD
    impact_confidence = Column(Float, nullable=True)  # 0-1 confidence score
    affected_industries = Column(JSONB, nullable=True)  # List of affected industries
    
    # Relationships
    category_id = Column(Integer, ForeignKey("policy_categories.id"), nullable=True)
    category = relationship("PolicyCategory", back_populates="policies")
    changes = relationship("PolicyChange", back_populates="policy")
    impact_assessments = relationship("ImpactAssessment", back_populates="policy")


class PolicyChange(Base):
    """Policy change tracking model."""
    __tablename__ = "policy_changes"
    
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    change_type = Column(String(50), nullable=False)  # amendment, repeal, extension, etc.
    change_date = Column(DateTime, nullable=False)
    change_description = Column(Text, nullable=True)
    
    # Impact of the change
    impact_magnitude = Column(Float, nullable=True)  # -1 to 1 scale
    impact_direction = Column(String(20), nullable=True)  # positive, negative, neutral
    
    # Source information
    source_document = Column(String(500), nullable=True)
    legislative_session = Column(String(100), nullable=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="changes")


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class PolicyCategorySchema(BaseModel):
    """Policy category schema."""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class PolicySchema(BaseModel):
    """Policy schema."""
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    policy_number: str
    jurisdiction: str
    policy_type: PolicyType
    status: PolicyStatus = PolicyStatus.DRAFT
    
    proposed_date: Optional[datetime] = None
    enacted_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    
    regulatory_body: Optional[str] = None
    authority: Optional[str] = None
    
    content_summary: Optional[str] = None
    full_text_url: Optional[str] = None
    source_url: Optional[str] = None
    
    estimated_impact: Optional[float] = None
    impact_confidence: Optional[float] = None
    affected_industries: Optional[List[str]] = None
    
    category_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class PolicyChangeSchema(BaseModel):
    """Policy change schema."""
    id: Optional[int] = None
    policy_id: int
    change_type: str
    change_date: datetime
    change_description: Optional[str] = None
    
    impact_magnitude: Optional[float] = None
    impact_direction: Optional[str] = None
    
    source_document: Optional[str] = None
    legislative_session: Optional[str] = None
    
    class Config:
        from_attributes = True 