"""
Market data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class MarketData(Base):
    """Market data model."""
    __tablename__ = "market_data"
    
    # Asset identification
    symbol = Column(String(50), nullable=False, index=True)
    asset_type = Column(String(50), nullable=False)  # stock, bond, commodity, currency, etc.
    exchange = Column(String(50), nullable=True)
    
    # Date and time
    date = Column(DateTime, nullable=False, index=True)
    timezone = Column(String(20), nullable=True, default="UTC")
    
    # Price data
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    adjusted_close = Column(Float, nullable=True)
    
    # Volume and trading
    volume = Column(Float, nullable=True)
    average_volume = Column(Float, nullable=True)
    
    # Returns and volatility
    daily_return = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    
    # Market cap and other metrics
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    
    # Source information
    data_source = Column(String(100), nullable=True)
    last_updated = Column(DateTime, nullable=True)


class EconomicIndicator(Base):
    """Economic indicator model."""
    __tablename__ = "economic_indicators"
    
    # Indicator details
    indicator_name = Column(String(200), nullable=False, index=True)
    indicator_code = Column(String(50), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True)  # GDP, inflation, employment, etc.
    subcategory = Column(String(100), nullable=True)
    
    # Geographic scope
    country = Column(String(10), nullable=False, index=True)
    region = Column(String(50), nullable=True)
    
    # Date and frequency
    date = Column(DateTime, nullable=False, index=True)
    frequency = Column(String(20), nullable=True)  # daily, weekly, monthly, quarterly, annual
    
    # Values
    value = Column(Float, nullable=True)
    previous_value = Column(Float, nullable=True)
    change = Column(Float, nullable=True)
    change_percentage = Column(Float, nullable=True)
    
    # Units and scaling
    unit = Column(String(50), nullable=True)  # USD, percentage, index, etc.
    scale = Column(String(20), nullable=True)  # millions, billions, etc.
    
    # Seasonality and adjustments
    is_seasonally_adjusted = Column(Boolean, nullable=True)
    is_annualized = Column(Boolean, nullable=True)
    
    # Confidence and reliability
    confidence_interval_lower = Column(Float, nullable=True)
    confidence_interval_upper = Column(Float, nullable=True)
    reliability_score = Column(Float, nullable=True)  # 0-1 score
    
    # Source information
    source_agency = Column(String(200), nullable=True)
    release_date = Column(DateTime, nullable=True)
    next_release_date = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)


class TradeFlow(Base):
    """Trade flow model."""
    __tablename__ = "trade_flows"
    
    # Trade identification
    trade_id = Column(String(100), unique=True, nullable=False, index=True)
    trade_type = Column(String(50), nullable=False)  # import, export, re-export
    
    # Geographic information
    origin_country = Column(String(10), nullable=False, index=True)
    destination_country = Column(String(10), nullable=False, index=True)
    transit_countries = Column(JSONB, nullable=True)  # List of transit countries
    
    # Product information
    product_category = Column(String(100), nullable=True)
    product_code = Column(String(50), nullable=True)  # HS code, SITC code, etc.
    product_description = Column(Text, nullable=True)
    
    # Trade details
    date = Column(DateTime, nullable=False, index=True)
    quantity = Column(Float, nullable=True)
    quantity_unit = Column(String(20), nullable=True)  # tons, pieces, liters, etc.
    value_usd = Column(Float, nullable=True)  # Value in USD
    value_local = Column(Float, nullable=True)  # Value in local currency
    local_currency = Column(String(10), nullable=True)
    
    # Tariff and duty information
    tariff_rate = Column(Float, nullable=True)  # Percentage
    duty_amount = Column(Float, nullable=True)  # In USD
    preferential_treatment = Column(Boolean, nullable=True)
    
    # Transportation
    transport_mode = Column(String(50), nullable=True)  # sea, air, land, rail
    shipping_route = Column(String(200), nullable=True)
    transit_time_days = Column(Integer, nullable=True)
    
    # Company information (if available)
    exporter_company = Column(String(200), nullable=True)
    importer_company = Column(String(200), nullable=True)
    
    # Policy impact
    affected_by_policies = Column(JSONB, nullable=True)  # List of affecting policies
    policy_impact_amount = Column(Float, nullable=True)  # Impact in USD
    
    # Source information
    data_source = Column(String(100), nullable=True)
    reporting_agency = Column(String(200), nullable=True)


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class MarketDataSchema(BaseModel):
    """Market data schema."""
    id: Optional[int] = None
    symbol: str
    asset_type: str
    exchange: Optional[str] = None
    
    date: datetime
    timezone: Optional[str] = "UTC"
    
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    adjusted_close: Optional[float] = None
    
    volume: Optional[float] = None
    average_volume: Optional[float] = None
    
    daily_return: Optional[float] = None
    volatility: Optional[float] = None
    
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    
    data_source: Optional[str] = None
    last_updated: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EconomicIndicatorSchema(BaseModel):
    """Economic indicator schema."""
    id: Optional[int] = None
    indicator_name: str
    indicator_code: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    
    country: str
    region: Optional[str] = None
    
    date: datetime
    frequency: Optional[str] = None
    
    value: Optional[float] = None
    previous_value: Optional[float] = None
    change: Optional[float] = None
    change_percentage: Optional[float] = None
    
    unit: Optional[str] = None
    scale: Optional[str] = None
    
    is_seasonally_adjusted: Optional[bool] = None
    is_annualized: Optional[bool] = None
    
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    reliability_score: Optional[float] = None
    
    source_agency: Optional[str] = None
    release_date: Optional[datetime] = None
    next_release_date: Optional[datetime] = None
    
    notes: Optional[str] = None
    methodology: Optional[str] = None
    
    class Config:
        from_attributes = True


class TradeFlowSchema(BaseModel):
    """Trade flow schema."""
    id: Optional[int] = None
    trade_id: str
    trade_type: str
    
    origin_country: str
    destination_country: str
    transit_countries: Optional[List[str]] = None
    
    product_category: Optional[str] = None
    product_code: Optional[str] = None
    product_description: Optional[str] = None
    
    date: datetime
    quantity: Optional[float] = None
    quantity_unit: Optional[str] = None
    value_usd: Optional[float] = None
    value_local: Optional[float] = None
    local_currency: Optional[str] = None
    
    tariff_rate: Optional[float] = None
    duty_amount: Optional[float] = None
    preferential_treatment: Optional[bool] = None
    
    transport_mode: Optional[str] = None
    shipping_route: Optional[str] = None
    transit_time_days: Optional[int] = None
    
    exporter_company: Optional[str] = None
    importer_company: Optional[str] = None
    
    affected_by_policies: Optional[List[str]] = None
    policy_impact_amount: Optional[float] = None
    
    data_source: Optional[str] = None
    reporting_agency: Optional[str] = None
    
    class Config:
        from_attributes = True 