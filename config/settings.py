"""
Configuration settings for PolicyRadar application.
"""
from typing import List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "PolicyRadar"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database
    database_url: str = Field(
        default="postgresql://policyradar:password@localhost:5432/policyradar",
        env="DATABASE_URL"
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    # Dashboard
    dashboard_host: str = Field(default="0.0.0.0", env="DASHBOARD_HOST")
    dashboard_port: int = Field(default=8501, env="DASHBOARD_PORT")
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    bloomberg_api_key: str = Field(default="", env="BLOOMBERG_API_KEY")
    reuters_api_key: str = Field(default="", env="REUTERS_API_KEY")
    quandl_api_key: str = Field(default="", env="QUANDL_API_KEY")
    
    # Data Sources
    policy_data_sources: List[str] = [
        "congress.gov",
        "federalregister.gov",
        "ec.europa.eu",
        "bankofengland.co.uk",
        "boj.or.jp",
        "ecb.europa.eu",
        "federalreserve.gov",
        "treasury.gov",
        "sec.gov",
        "cfpb.gov",
        "epa.gov",
        "irs.gov",
        "ustr.gov",
        "commerce.gov",
        "energy.gov"
    ]
    
    # Jurisdictions
    jurisdictions: List[str] = [
        "US", "EU", "UK", "JP", "CA", "AU", "CN", "IN", "BR", "MX",
        "DE", "FR", "IT", "ES", "NL", "SE", "CH", "NO", "DK", "FI",
        "SG", "HK", "KR", "TW", "TH", "MY", "ID", "PH", "VN", "IN",
        "ZA", "EG", "NG", "KE", "GH", "MA", "TN", "DZ", "ET", "UG",
        "TZ", "ZM", "ZW", "BW", "NA", "LS", "SZ", "MW", "MZ", "AO"
    ]
    
    # Industries
    industries: List[str] = [
        "financial_services", "technology", "energy", "healthcare",
        "manufacturing", "retail", "telecommunications", "transportation",
        "real_estate", "utilities", "materials", "consumer_goods",
        "industrials", "media", "aerospace", "defense", "pharmaceuticals",
        "biotechnology", "automotive", "chemicals"
    ]
    
    # Model Parameters
    prediction_horizon_months: int = 12
    confidence_threshold: float = 0.7
    impact_accuracy_target: float = 0.85
    
    # Data Processing
    batch_size: int = 1000
    max_workers: int = 4
    cache_ttl_seconds: int = 3600
    
    # Monitoring
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    # File Paths
    data_dir: str = Field(default="./data", env="DATA_DIR")
    models_dir: str = Field(default="./models", env="MODELS_DIR")
    logs_dir: str = Field(default="./logs", env="LOGS_DIR")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Industry-specific configurations
INDUSTRY_CONFIGS = {
    "financial_services": {
        "regulations": ["basel_iii", "dodd_frank", "mifid_ii", "gdpr", "sox"],
        "risk_factors": ["capital_requirements", "liquidity_ratios", "stress_testing"],
        "impact_metrics": ["capital_adequacy", "profitability", "market_risk"]
    },
    "technology": {
        "regulations": ["gdpr", "ccpa", "antitrust", "ai_regulation", "cybersecurity"],
        "risk_factors": ["data_privacy", "market_dominance", "algorithmic_bias"],
        "impact_metrics": ["compliance_costs", "market_share", "innovation_pipeline"]
    },
    "energy": {
        "regulations": ["carbon_pricing", "renewable_incentives", "emissions_trading"],
        "risk_factors": ["carbon_tax", "renewable_targets", "grid_modernization"],
        "impact_metrics": ["emissions_reduction", "renewable_investment", "energy_efficiency"]
    },
    "healthcare": {
        "regulations": ["drug_pricing", "interoperability", "telehealth", "privacy"],
        "risk_factors": ["reimbursement_changes", "approval_processes", "data_sharing"],
        "impact_metrics": ["revenue_impact", "compliance_costs", "patient_outcomes"]
    },
    "manufacturing": {
        "regulations": ["trade_tariffs", "environmental_standards", "labor_laws"],
        "risk_factors": ["supply_chain_disruption", "cost_inflation", "regulatory_compliance"],
        "impact_metrics": ["production_costs", "supply_chain_efficiency", "market_access"]
    }
}

# Policy categories
POLICY_CATEGORIES = {
    "trade": ["tariffs", "quotas", "trade_agreements", "export_controls"],
    "financial": ["capital_requirements", "liquidity_rules", "stress_testing", "reporting"],
    "environmental": ["carbon_pricing", "emissions_standards", "renewable_targets"],
    "tax": ["corporate_tax", "transfer_pricing", "tax_incentives", "withholding_tax"],
    "labor": ["minimum_wage", "workplace_safety", "union_rights", "immigration"],
    "technology": ["data_privacy", "ai_regulation", "cybersecurity", "antitrust"],
    "healthcare": ["drug_pricing", "insurance_reform", "telehealth", "approval_processes"]
}

# Risk levels
RISK_LEVELS = {
    "low": {"score": 1, "color": "#28a745", "description": "Minimal impact expected"},
    "medium": {"score": 2, "color": "#ffc107", "description": "Moderate impact expected"},
    "high": {"score": 3, "color": "#fd7e14", "description": "Significant impact expected"},
    "critical": {"score": 4, "color": "#dc3545", "description": "Severe impact expected"}
} 