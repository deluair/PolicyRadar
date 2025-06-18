"""
Company-related data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class Company(Base):
    """Company model."""
    __tablename__ = "companies"
    
    name = Column(String(200), nullable=False, index=True)
    ticker_symbol = Column(String(20), unique=True, nullable=True, index=True)
    isin = Column(String(20), unique=True, nullable=True, index=True)
    cusip = Column(String(20), unique=True, nullable=True, index=True)
    
    # Company details
    industry = Column(String(100), nullable=False, index=True)
    sector = Column(String(100), nullable=True)
    sub_sector = Column(String(100), nullable=True)
    
    # Location
    headquarters_country = Column(String(10), nullable=False, index=True)
    headquarters_city = Column(String(100), nullable=True)
    incorporation_country = Column(String(10), nullable=True)
    
    # Company size
    market_cap = Column(Float, nullable=True)  # In millions USD
    revenue = Column(Float, nullable=True)  # In millions USD
    employees = Column(Integer, nullable=True)
    
    # Fortune 500 status
    fortune_500_rank = Column(Integer, nullable=True)
    fortune_500_year = Column(Integer, nullable=True)
    
    # Business model
    business_model = Column(String(100), nullable=True)
    primary_markets = Column(JSONB, nullable=True)  # List of primary markets
    supply_chain_exposure = Column(JSONB, nullable=True)  # Supply chain details
    
    # Regulatory exposure
    regulatory_jurisdictions = Column(JSONB, nullable=True)  # List of jurisdictions
    compliance_requirements = Column(JSONB, nullable=True)  # Compliance details
    
    # Relationships
    profile = relationship("CompanyProfile", back_populates="company", uselist=False)
    financial_metrics = relationship("FinancialMetrics", back_populates="company")
    impact_assessments = relationship("ImpactAssessment", back_populates="company")


class CompanyProfile(Base):
    """Detailed company profile model."""
    __tablename__ = "company_profiles"
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Company description
    description = Column(Text, nullable=True)
    mission_statement = Column(Text, nullable=True)
    vision_statement = Column(Text, nullable=True)
    
    # Key executives
    ceo = Column(String(100), nullable=True)
    cfo = Column(String(100), nullable=True)
    general_counsel = Column(String(100), nullable=True)
    
    # Contact information
    website = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    
    # Social responsibility
    esg_rating = Column(String(10), nullable=True)
    sustainability_goals = Column(JSONB, nullable=True)
    carbon_footprint = Column(Float, nullable=True)  # In metric tons CO2
    
    # Risk profile
    risk_tolerance = Column(String(20), nullable=True)  # low, medium, high
    political_exposure = Column(Float, nullable=True)  # 0-1 scale
    regulatory_risk_score = Column(Float, nullable=True)  # 0-1 scale
    
    # Relationships
    company = relationship("Company", back_populates="profile")


class FinancialMetrics(Base):
    """Financial metrics model."""
    __tablename__ = "financial_metrics"
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    
    # Revenue metrics
    total_revenue = Column(Float, nullable=True)  # In millions USD
    revenue_growth = Column(Float, nullable=True)  # Percentage
    revenue_by_region = Column(JSONB, nullable=True)  # Regional breakdown
    
    # Profitability metrics
    net_income = Column(Float, nullable=True)  # In millions USD
    operating_income = Column(Float, nullable=True)  # In millions USD
    ebitda = Column(Float, nullable=True)  # In millions USD
    profit_margin = Column(Float, nullable=True)  # Percentage
    
    # Balance sheet metrics
    total_assets = Column(Float, nullable=True)  # In millions USD
    total_liabilities = Column(Float, nullable=True)  # In millions USD
    shareholders_equity = Column(Float, nullable=True)  # In millions USD
    debt_to_equity = Column(Float, nullable=True)  # Ratio
    
    # Cash flow metrics
    operating_cash_flow = Column(Float, nullable=True)  # In millions USD
    investing_cash_flow = Column(Float, nullable=True)  # In millions USD
    financing_cash_flow = Column(Float, nullable=True)  # In millions USD
    free_cash_flow = Column(Float, nullable=True)  # In millions USD
    
    # Market metrics
    market_cap = Column(Float, nullable=True)  # In millions USD
    enterprise_value = Column(Float, nullable=True)  # In millions USD
    pe_ratio = Column(Float, nullable=True)  # Price to earnings
    pb_ratio = Column(Float, nullable=True)  # Price to book
    
    # Regulatory capital (for financial institutions)
    tier_1_capital = Column(Float, nullable=True)  # In millions USD
    tier_2_capital = Column(Float, nullable=True)  # In millions USD
    risk_weighted_assets = Column(Float, nullable=True)  # In millions USD
    capital_adequacy_ratio = Column(Float, nullable=True)  # Percentage
    
    # Tax metrics
    effective_tax_rate = Column(Float, nullable=True)  # Percentage
    tax_expense = Column(Float, nullable=True)  # In millions USD
    deferred_tax_assets = Column(Float, nullable=True)  # In millions USD
    deferred_tax_liabilities = Column(Float, nullable=True)  # In millions USD
    
    # Relationships
    company = relationship("Company", back_populates="financial_metrics")


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class CompanySchema(BaseModel):
    """Company schema."""
    id: Optional[int] = None
    name: str
    ticker_symbol: Optional[str] = None
    isin: Optional[str] = None
    cusip: Optional[str] = None
    
    industry: str
    sector: Optional[str] = None
    sub_sector: Optional[str] = None
    
    headquarters_country: str
    headquarters_city: Optional[str] = None
    incorporation_country: Optional[str] = None
    
    market_cap: Optional[float] = None
    revenue: Optional[float] = None
    employees: Optional[int] = None
    
    fortune_500_rank: Optional[int] = None
    fortune_500_year: Optional[int] = None
    
    business_model: Optional[str] = None
    primary_markets: Optional[List[str]] = None
    supply_chain_exposure: Optional[dict] = None
    
    regulatory_jurisdictions: Optional[List[str]] = None
    compliance_requirements: Optional[dict] = None
    
    class Config:
        from_attributes = True


class CompanyProfileSchema(BaseModel):
    """Company profile schema."""
    id: Optional[int] = None
    company_id: int
    
    description: Optional[str] = None
    mission_statement: Optional[str] = None
    vision_statement: Optional[str] = None
    
    ceo: Optional[str] = None
    cfo: Optional[str] = None
    general_counsel: Optional[str] = None
    
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    esg_rating: Optional[str] = None
    sustainability_goals: Optional[dict] = None
    carbon_footprint: Optional[float] = None
    
    risk_tolerance: Optional[str] = None
    political_exposure: Optional[float] = None
    regulatory_risk_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class FinancialMetricsSchema(BaseModel):
    """Financial metrics schema."""
    id: Optional[int] = None
    company_id: int
    date: datetime
    
    total_revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    revenue_by_region: Optional[dict] = None
    
    net_income: Optional[float] = None
    operating_income: Optional[float] = None
    ebitda: Optional[float] = None
    profit_margin: Optional[float] = None
    
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    shareholders_equity: Optional[float] = None
    debt_to_equity: Optional[float] = None
    
    operating_cash_flow: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    
    tier_1_capital: Optional[float] = None
    tier_2_capital: Optional[float] = None
    risk_weighted_assets: Optional[float] = None
    capital_adequacy_ratio: Optional[float] = None
    
    effective_tax_rate: Optional[float] = None
    tax_expense: Optional[float] = None
    deferred_tax_assets: Optional[float] = None
    deferred_tax_liabilities: Optional[float] = None
    
    class Config:
        from_attributes = True 