"""
Regulatory data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from .base import Base


class RegulatoryType(enum.Enum):
    """Regulatory type enumeration."""
    CENTRAL_BANK = "central_bank"
    SECURITIES_REGULATOR = "securities_regulator"
    BANKING_REGULATOR = "banking_regulator"
    INSURANCE_REGULATOR = "insurance_regulator"
    ENVIRONMENTAL_AGENCY = "environmental_agency"
    TAX_AUTHORITY = "tax_authority"
    TRADE_AUTHORITY = "trade_authority"
    COMPETITION_AUTHORITY = "competition_authority"
    DATA_PROTECTION_AUTHORITY = "data_protection_authority"
    HEALTH_REGULATOR = "health_regulator"
    OTHER = "other"


class ComplianceStatus(enum.Enum):
    """Compliance status enumeration."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    PENDING_REVIEW = "pending_review"
    EXEMPT = "exempt"
    NOT_APPLICABLE = "not_applicable"


class RegulatoryBody(Base):
    """Regulatory body model."""
    __tablename__ = "regulatory_bodies"
    
    # Basic information
    name = Column(String(200), nullable=False, index=True)
    short_name = Column(String(50), nullable=True)
    regulatory_type = Column(Enum(RegulatoryType), nullable=False)
    
    # Geographic scope
    country = Column(String(10), nullable=False, index=True)
    region = Column(String(50), nullable=True)
    jurisdiction = Column(String(200), nullable=True)
    
    # Contact and location
    website = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    
    # Authority and powers
    legal_basis = Column(Text, nullable=True)
    enforcement_powers = Column(JSONB, nullable=True)  # List of enforcement powers
    penalty_authority = Column(JSONB, nullable=True)  # Penalty information
    
    # Leadership
    chairperson = Column(String(100), nullable=True)
    director_general = Column(String(100), nullable=True)
    board_size = Column(Integer, nullable=True)
    
    # Budget and resources
    annual_budget = Column(Float, nullable=True)  # In millions USD
    staff_count = Column(Integer, nullable=True)
    
    # Regulatory activities
    policies_issued = Column(Integer, nullable=True)
    enforcement_actions = Column(Integer, nullable=True)
    last_activity_date = Column(DateTime, nullable=True)
    
    # Relationships
    compliance_requirements = relationship("ComplianceRequirement", back_populates="regulatory_body")


class ComplianceRequirement(Base):
    """Compliance requirement model."""
    __tablename__ = "compliance_requirements"
    
    regulatory_body_id = Column(Integer, ForeignKey("regulatory_bodies.id"), nullable=False)
    
    # Requirement details
    requirement_name = Column(String(200), nullable=False, index=True)
    requirement_code = Column(String(100), nullable=True, unique=True)
    description = Column(Text, nullable=True)
    
    # Applicability
    applicable_industries = Column(JSONB, nullable=True)  # List of applicable industries
    applicable_companies = Column(JSONB, nullable=True)  # List of applicable company types
    threshold_criteria = Column(JSONB, nullable=True)  # Size, revenue, etc. thresholds
    
    # Timeline
    effective_date = Column(DateTime, nullable=True)
    compliance_deadline = Column(DateTime, nullable=True)
    review_frequency = Column(String(50), nullable=True)  # annual, quarterly, etc.
    
    # Requirements
    reporting_requirements = Column(JSONB, nullable=True)  # Reporting details
    documentation_requirements = Column(JSONB, nullable=True)  # Documentation needed
    testing_requirements = Column(JSONB, nullable=True)  # Testing requirements
    
    # Compliance costs
    estimated_compliance_cost = Column(Float, nullable=True)  # In millions USD
    ongoing_maintenance_cost = Column(Float, nullable=True)  # Annual cost
    implementation_timeline = Column(Integer, nullable=True)  # In months
    
    # Penalties and enforcement
    penalty_structure = Column(JSONB, nullable=True)  # Penalty details
    enforcement_mechanisms = Column(JSONB, nullable=True)  # How enforced
    appeal_process = Column(Text, nullable=True)
    
    # Status and monitoring
    current_status = Column(Enum(ComplianceStatus), nullable=True)
    last_review_date = Column(DateTime, nullable=True)
    next_review_date = Column(DateTime, nullable=True)
    
    # Related policies
    related_policies = Column(JSONB, nullable=True)  # List of related policy IDs
    superseded_requirements = Column(JSONB, nullable=True)  # Requirements this replaces
    
    # Relationships
    regulatory_body = relationship("RegulatoryBody", back_populates="compliance_requirements")


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class RegulatoryBodySchema(BaseModel):
    """Regulatory body schema."""
    id: Optional[int] = None
    name: str
    short_name: Optional[str] = None
    regulatory_type: RegulatoryType
    
    country: str
    region: Optional[str] = None
    jurisdiction: Optional[str] = None
    
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    legal_basis: Optional[str] = None
    enforcement_powers: Optional[List[str]] = None
    penalty_authority: Optional[dict] = None
    
    chairperson: Optional[str] = None
    director_general: Optional[str] = None
    board_size: Optional[int] = None
    
    annual_budget: Optional[float] = None
    staff_count: Optional[int] = None
    
    policies_issued: Optional[int] = None
    enforcement_actions: Optional[int] = None
    last_activity_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplianceRequirementSchema(BaseModel):
    """Compliance requirement schema."""
    id: Optional[int] = None
    regulatory_body_id: int
    
    requirement_name: str
    requirement_code: Optional[str] = None
    description: Optional[str] = None
    
    applicable_industries: Optional[List[str]] = None
    applicable_companies: Optional[List[str]] = None
    threshold_criteria: Optional[dict] = None
    
    effective_date: Optional[datetime] = None
    compliance_deadline: Optional[datetime] = None
    review_frequency: Optional[str] = None
    
    reporting_requirements: Optional[dict] = None
    documentation_requirements: Optional[dict] = None
    testing_requirements: Optional[dict] = None
    
    estimated_compliance_cost: Optional[float] = None
    ongoing_maintenance_cost: Optional[float] = None
    implementation_timeline: Optional[int] = None
    
    penalty_structure: Optional[dict] = None
    enforcement_mechanisms: Optional[dict] = None
    appeal_process: Optional[str] = None
    
    current_status: Optional[ComplianceStatus] = None
    last_review_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    
    related_policies: Optional[List[int]] = None
    superseded_requirements: Optional[List[int]] = None
    
    class Config:
        from_attributes = True 