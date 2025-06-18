"""
Impact assessment data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from .base import Base


class ImpactDirection(enum.Enum):
    """Impact direction enumeration."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class RiskLevel(enum.Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImpactAssessment(Base):
    """Policy impact assessment model."""
    __tablename__ = "impact_assessments"
    
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Assessment details
    assessment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    assessment_period = Column(String(50), nullable=True)  # e.g., "2025-2026"
    scenario = Column(String(100), nullable=True)  # e.g., "baseline", "worst_case"
    
    # Overall impact
    overall_impact = Column(Float, nullable=True)  # In millions USD
    impact_direction = Column(Enum(ImpactDirection), nullable=True)
    confidence_level = Column(Float, nullable=True)  # 0-1 confidence score
    
    # Impact breakdown
    revenue_impact = Column(Float, nullable=True)  # In millions USD
    cost_impact = Column(Float, nullable=True)  # In millions USD
    capital_impact = Column(Float, nullable=True)  # In millions USD
    tax_impact = Column(Float, nullable=True)  # In millions USD
    
    # Risk assessment
    risk_level = Column(Enum(RiskLevel), nullable=True)
    risk_score = Column(Float, nullable=True)  # 0-1 risk score
    risk_factors = Column(JSONB, nullable=True)  # List of risk factors
    
    # Implementation timeline
    implementation_date = Column(DateTime, nullable=True)
    compliance_deadline = Column(DateTime, nullable=True)
    transition_period = Column(Integer, nullable=True)  # In months
    
    # Mitigation strategies
    mitigation_strategies = Column(JSONB, nullable=True)  # List of strategies
    mitigation_cost = Column(Float, nullable=True)  # In millions USD
    mitigation_effectiveness = Column(Float, nullable=True)  # 0-1 effectiveness
    
    # Notes and analysis
    analysis_summary = Column(Text, nullable=True)
    key_assumptions = Column(JSONB, nullable=True)
    sensitivity_analysis = Column(JSONB, nullable=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="impact_assessments")
    company = relationship("Company", back_populates="impact_assessments")
    metrics = relationship("ImpactMetric", back_populates="assessment")
    risk_scores = relationship("RiskScore", back_populates="assessment")


class ImpactMetric(Base):
    """Detailed impact metrics model."""
    __tablename__ = "impact_metrics"
    
    assessment_id = Column(Integer, ForeignKey("impact_assessments.id"), nullable=False)
    
    # Metric details
    metric_name = Column(String(100), nullable=False)
    metric_category = Column(String(100), nullable=True)  # financial, operational, strategic
    metric_unit = Column(String(50), nullable=True)  # USD, percentage, ratio, etc.
    
    # Values
    baseline_value = Column(Float, nullable=True)
    projected_value = Column(Float, nullable=True)
    change_amount = Column(Float, nullable=True)
    change_percentage = Column(Float, nullable=True)
    
    # Time series
    time_period = Column(String(50), nullable=True)  # e.g., "Q1 2025", "2025"
    quarterly_values = Column(JSONB, nullable=True)  # Quarterly breakdown
    annual_values = Column(JSONB, nullable=True)  # Annual breakdown
    
    # Confidence and uncertainty
    confidence_interval_lower = Column(Float, nullable=True)
    confidence_interval_upper = Column(Float, nullable=True)
    uncertainty_factors = Column(JSONB, nullable=True)
    
    # Relationships
    assessment = relationship("ImpactAssessment", back_populates="metrics")


class RiskScore(Base):
    """Risk scoring model."""
    __tablename__ = "risk_scores"
    
    assessment_id = Column(Integer, ForeignKey("impact_assessments.id"), nullable=False)
    
    # Risk details
    risk_category = Column(String(100), nullable=False)  # regulatory, operational, financial, etc.
    risk_factor = Column(String(200), nullable=False)
    risk_description = Column(Text, nullable=True)
    
    # Scoring
    probability_score = Column(Float, nullable=True)  # 0-1 probability
    severity_score = Column(Float, nullable=True)  # 0-1 severity
    overall_risk_score = Column(Float, nullable=True)  # probability * severity
    risk_level = Column(Enum(RiskLevel), nullable=True)
    
    # Mitigation
    mitigation_measures = Column(JSONB, nullable=True)
    residual_risk_score = Column(Float, nullable=True)  # After mitigation
    
    # Monitoring
    monitoring_frequency = Column(String(50), nullable=True)  # daily, weekly, monthly
    trigger_conditions = Column(JSONB, nullable=True)  # Conditions that trigger review
    
    # Relationships
    assessment = relationship("ImpactAssessment", back_populates="risk_scores")


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class ImpactAssessmentSchema(BaseModel):
    """Impact assessment schema."""
    id: Optional[int] = None
    policy_id: int
    company_id: int
    
    assessment_date: datetime
    assessment_period: Optional[str] = None
    scenario: Optional[str] = None
    
    overall_impact: Optional[float] = None
    impact_direction: Optional[ImpactDirection] = None
    confidence_level: Optional[float] = None
    
    revenue_impact: Optional[float] = None
    cost_impact: Optional[float] = None
    capital_impact: Optional[float] = None
    tax_impact: Optional[float] = None
    
    risk_level: Optional[RiskLevel] = None
    risk_score: Optional[float] = None
    risk_factors: Optional[List[str]] = None
    
    implementation_date: Optional[datetime] = None
    compliance_deadline: Optional[datetime] = None
    transition_period: Optional[int] = None
    
    mitigation_strategies: Optional[List[str]] = None
    mitigation_cost: Optional[float] = None
    mitigation_effectiveness: Optional[float] = None
    
    analysis_summary: Optional[str] = None
    key_assumptions: Optional[dict] = None
    sensitivity_analysis: Optional[dict] = None
    
    class Config:
        from_attributes = True


class ImpactMetricSchema(BaseModel):
    """Impact metric schema."""
    id: Optional[int] = None
    assessment_id: int
    
    metric_name: str
    metric_category: Optional[str] = None
    metric_unit: Optional[str] = None
    
    baseline_value: Optional[float] = None
    projected_value: Optional[float] = None
    change_amount: Optional[float] = None
    change_percentage: Optional[float] = None
    
    time_period: Optional[str] = None
    quarterly_values: Optional[dict] = None
    annual_values: Optional[dict] = None
    
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    uncertainty_factors: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class RiskScoreSchema(BaseModel):
    """Risk score schema."""
    id: Optional[int] = None
    assessment_id: int
    
    risk_category: str
    risk_factor: str
    risk_description: Optional[str] = None
    
    probability_score: Optional[float] = None
    severity_score: Optional[float] = None
    overall_risk_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = None
    
    mitigation_measures: Optional[List[str]] = None
    residual_risk_score: Optional[float] = None
    
    monitoring_frequency: Optional[str] = None
    trigger_conditions: Optional[dict] = None
    
    class Config:
        from_attributes = True 