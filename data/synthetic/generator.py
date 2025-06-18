"""
Main synthetic data generator for PolicyRadar.
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from loguru import logger

from config.settings import settings
from data.models import (
    Policy, PolicyCategory, PolicyChange,
    Company, CompanyProfile, FinancialMetrics,
    ImpactAssessment, ImpactMetric, RiskScore,
    MarketData, EconomicIndicator, TradeFlow,
    RegulatoryBody, ComplianceRequirement,
    PolicyPrediction, PredictionModel
)
from .policy_data import PolicyDataGenerator
from .company_data import CompanyDataGenerator
from .market_data import MarketDataGenerator
from .impact_data import ImpactDataGenerator


class SyntheticDataGenerator:
    """Main synthetic data generator for PolicyRadar."""
    
    def __init__(self, output_dir: str = None):
        """Initialize the synthetic data generator."""
        self.output_dir = output_dir or settings.data_dir
        self.ensure_output_dir()
        
        # Initialize sub-generators
        self.policy_generator = PolicyDataGenerator()
        self.company_generator = CompanyDataGenerator()
        self.market_generator = MarketDataGenerator()
        self.impact_generator = ImpactDataGenerator()
        
        logger.info(f"Synthetic data generator initialized with output directory: {self.output_dir}")
    
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "policies"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "companies"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "market_data"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "impacts"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "regulatory"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "predictions"), exist_ok=True)
    
    def generate_all_data(self, 
                         num_policies: int = 1000,
                         num_companies: int = 500,
                         num_market_records: int = 10000,
                         start_date: datetime = None,
                         end_date: datetime = None) -> Dict[str, Any]:
        """
        Generate all synthetic data for PolicyRadar.
        
        Args:
            num_policies: Number of policies to generate
            num_companies: Number of companies to generate
            num_market_records: Number of market data records to generate
            start_date: Start date for data generation
            end_date: End date for data generation
            
        Returns:
            Dictionary containing all generated data
        """
        logger.info("Starting comprehensive synthetic data generation...")
        
        # Set default date range if not provided
        if not start_date:
            start_date = datetime(2015, 1, 1)
        if not end_date:
            end_date = datetime(2025, 12, 31)
        
        # Generate data
        data = {}
        
        # 1. Generate policy categories
        logger.info("Generating policy categories...")
        data['policy_categories'] = self.policy_generator.generate_categories()
        
        # 2. Generate policies
        logger.info(f"Generating {num_policies} policies...")
        data['policies'] = self.policy_generator.generate_policies(
            num_policies, start_date, end_date, data['policy_categories']
        )
        
        # 3. Generate policy changes
        logger.info("Generating policy changes...")
        data['policy_changes'] = self.policy_generator.generate_policy_changes(
            data['policies'], start_date, end_date
        )
        
        # 4. Generate companies
        logger.info(f"Generating {num_companies} companies...")
        data['companies'] = self.company_generator.generate_companies(num_companies)
        
        # 5. Generate company profiles
        logger.info("Generating company profiles...")
        data['company_profiles'] = self.company_generator.generate_company_profiles(
            data['companies']
        )
        
        # 6. Generate financial metrics
        logger.info("Generating financial metrics...")
        data['financial_metrics'] = self.company_generator.generate_financial_metrics(
            data['companies'], start_date, end_date
        )
        
        # 7. Generate market data
        logger.info(f"Generating {num_market_records} market data records...")
        data['market_data'] = self.market_generator.generate_market_data(
            num_market_records, start_date, end_date
        )
        
        # 8. Generate economic indicators
        logger.info("Generating economic indicators...")
        data['economic_indicators'] = self.market_generator.generate_economic_indicators(
            start_date, end_date
        )
        
        # 9. Generate trade flows
        logger.info("Generating trade flows...")
        data['trade_flows'] = self.market_generator.generate_trade_flows(
            data['companies'], start_date, end_date
        )
        
        # 10. Generate regulatory bodies
        logger.info("Generating regulatory bodies...")
        data['regulatory_bodies'] = self.generate_regulatory_bodies()
        
        # 11. Generate compliance requirements
        logger.info("Generating compliance requirements...")
        data['compliance_requirements'] = self.generate_compliance_requirements(
            data['regulatory_bodies'], data['policies']
        )
        
        # 12. Generate impact assessments
        logger.info("Generating impact assessments...")
        data['impact_assessments'] = self.impact_generator.generate_impact_assessments(
            data['policies'], data['companies'], start_date, end_date
        )
        
        # 13. Generate impact metrics
        logger.info("Generating impact metrics...")
        data['impact_metrics'] = self.impact_generator.generate_impact_metrics(
            data['impact_assessments']
        )
        
        # 14. Generate risk scores
        logger.info("Generating risk scores...")
        data['risk_scores'] = self.impact_generator.generate_risk_scores(
            data['impact_assessments']
        )
        
        # 15. Generate prediction models
        logger.info("Generating prediction models...")
        data['prediction_models'] = self.generate_prediction_models()
        
        # 16. Generate policy predictions
        logger.info("Generating policy predictions...")
        data['policy_predictions'] = self.generate_policy_predictions(
            data['policies'], data['prediction_models'], start_date, end_date
        )
        
        logger.info("Synthetic data generation completed successfully!")
        return data
    
    def save_data(self, data: Dict[str, Any], format: str = "json"):
        """
        Save generated data to files.
        
        Args:
            data: Dictionary containing all generated data
            format: Output format (json, csv, parquet)
        """
        logger.info(f"Saving data in {format} format...")
        
        for data_type, records in data.items():
            if not records:
                continue
                
            # Create DataFrame
            df = pd.DataFrame(records)
            
            # Determine output path
            output_path = os.path.join(self.output_dir, f"{data_type}.{format}")
            
            # Save based on format
            if format == "json":
                df.to_json(output_path, orient="records", indent=2)
            elif format == "csv":
                df.to_csv(output_path, index=False)
            elif format == "parquet":
                df.to_parquet(output_path, index=False)
            
            logger.info(f"Saved {len(records)} {data_type} records to {output_path}")
    
    def generate_regulatory_bodies(self) -> List[Dict[str, Any]]:
        """Generate synthetic regulatory bodies."""
        regulatory_bodies = []
        
        # Major regulatory bodies by country
        regulatory_data = {
            "US": [
                {"name": "Federal Reserve System", "type": "CENTRAL_BANK", "short_name": "Fed"},
                {"name": "Securities and Exchange Commission", "type": "SECURITIES_REGULATOR", "short_name": "SEC"},
                {"name": "Office of the Comptroller of the Currency", "type": "BANKING_REGULATOR", "short_name": "OCC"},
                {"name": "Environmental Protection Agency", "type": "ENVIRONMENTAL_AGENCY", "short_name": "EPA"},
                {"name": "Internal Revenue Service", "type": "TAX_AUTHORITY", "short_name": "IRS"},
            ],
            "EU": [
                {"name": "European Central Bank", "type": "CENTRAL_BANK", "short_name": "ECB"},
                {"name": "European Securities and Markets Authority", "type": "SECURITIES_REGULATOR", "short_name": "ESMA"},
                {"name": "European Banking Authority", "type": "BANKING_REGULATOR", "short_name": "EBA"},
                {"name": "European Environment Agency", "type": "ENVIRONMENTAL_AGENCY", "short_name": "EEA"},
            ],
            "UK": [
                {"name": "Bank of England", "type": "CENTRAL_BANK", "short_name": "BoE"},
                {"name": "Financial Conduct Authority", "type": "SECURITIES_REGULATOR", "short_name": "FCA"},
                {"name": "Prudential Regulation Authority", "type": "BANKING_REGULATOR", "short_name": "PRA"},
            ],
            "JP": [
                {"name": "Bank of Japan", "type": "CENTRAL_BANK", "short_name": "BoJ"},
                {"name": "Financial Services Agency", "type": "SECURITIES_REGULATOR", "short_name": "FSA"},
            ],
            "CN": [
                {"name": "People's Bank of China", "type": "CENTRAL_BANK", "short_name": "PBoC"},
                {"name": "China Securities Regulatory Commission", "type": "SECURITIES_REGULATOR", "short_name": "CSRC"},
            ]
        }
        
        for country, bodies in regulatory_data.items():
            for i, body in enumerate(bodies):
                regulatory_bodies.append({
                    "name": body["name"],
                    "short_name": body["short_name"],
                    "regulatory_type": body["type"],
                    "country": country,
                    "region": "Asia" if country in ["JP", "CN"] else "Europe" if country in ["EU", "UK"] else "Americas",
                    "website": f"https://www.{body['short_name'].lower()}.gov",
                    "annual_budget": np.random.uniform(100, 2000),
                    "staff_count": np.random.randint(500, 10000),
                    "policies_issued": np.random.randint(50, 500),
                    "enforcement_actions": np.random.randint(10, 200),
                    "last_activity_date": datetime.now() - timedelta(days=np.random.randint(1, 365))
                })
        
        return regulatory_bodies
    
    def generate_compliance_requirements(self, regulatory_bodies: List[Dict], policies: List[Dict]) -> List[Dict[str, Any]]:
        """Generate synthetic compliance requirements."""
        requirements = []
        
        requirement_templates = [
            {
                "name": "Capital Adequacy Requirements",
                "description": "Minimum capital requirements for financial institutions",
                "industries": ["financial_services"],
                "review_frequency": "quarterly"
            },
            {
                "name": "Environmental Impact Assessment",
                "description": "Environmental impact assessment for major projects",
                "industries": ["energy", "manufacturing"],
                "review_frequency": "annual"
            },
            {
                "name": "Data Privacy Compliance",
                "description": "Data protection and privacy requirements",
                "industries": ["technology", "healthcare", "financial_services"],
                "review_frequency": "annual"
            },
            {
                "name": "Tax Reporting Requirements",
                "description": "Comprehensive tax reporting and documentation",
                "industries": ["all"],
                "review_frequency": "quarterly"
            }
        ]
        
        for i, body in enumerate(regulatory_bodies):
            for template in requirement_templates:
                requirements.append({
                    "regulatory_body_id": i + 1,
                    "requirement_name": template["name"],
                    "requirement_code": f"REQ_{body['short_name']}_{i+1:03d}",
                    "description": template["description"],
                    "applicable_industries": template["industries"],
                    "effective_date": datetime.now() - timedelta(days=np.random.randint(100, 1000)),
                    "compliance_deadline": datetime.now() + timedelta(days=np.random.randint(30, 365)),
                    "review_frequency": template["review_frequency"],
                    "estimated_compliance_cost": np.random.uniform(1, 50),
                    "ongoing_maintenance_cost": np.random.uniform(0.1, 5),
                    "implementation_timeline": np.random.randint(3, 24),
                    "current_status": np.random.choice(["COMPLIANT", "NON_COMPLIANT", "PARTIALLY_COMPLIANT"])
                })
        
        return requirements
    
    def generate_prediction_models(self) -> List[Dict[str, Any]]:
        """Generate synthetic prediction models."""
        models = []
        
        model_templates = [
            {
                "name": "Policy Change Prediction Model",
                "type": "CLASSIFICATION",
                "algorithm": "XGBoost",
                "description": "Predicts likelihood of policy changes"
            },
            {
                "name": "Impact Forecasting Model",
                "type": "REGRESSION",
                "algorithm": "Random Forest",
                "description": "Forecasts financial impact of policy changes"
            },
            {
                "name": "Risk Assessment Model",
                "type": "CLASSIFICATION",
                "algorithm": "Logistic Regression",
                "description": "Assesses regulatory risk levels"
            },
            {
                "name": "Time Series Policy Model",
                "type": "TIME_SERIES",
                "algorithm": "LSTM",
                "description": "Time series analysis of policy trends"
            }
        ]
        
        for i, template in enumerate(model_templates):
            models.append({
                "model_name": template["name"],
                "model_type": template["type"],
                "model_version": f"v1.{i+1}.0",
                "description": template["description"],
                "algorithm": template["algorithm"],
                "training_data_size": np.random.randint(10000, 100000),
                "accuracy_score": np.random.uniform(0.75, 0.95),
                "precision_score": np.random.uniform(0.70, 0.90),
                "recall_score": np.random.uniform(0.70, 0.90),
                "f1_score": np.random.uniform(0.70, 0.90),
                "validation_method": "cross_validation",
                "validation_score": np.random.uniform(0.70, 0.90),
                "is_active": True,
                "deployment_date": datetime.now() - timedelta(days=np.random.randint(30, 365))
            })
        
        return models
    
    def generate_policy_predictions(self, policies: List[Dict], models: List[Dict], 
                                  start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic policy predictions."""
        predictions = []
        
        prediction_types = ["policy_change", "impact_forecast", "risk_assessment", "timeline_prediction"]
        
        for i, policy in enumerate(policies):
            for j, model in enumerate(models):
                prediction_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                target_date = prediction_date + timedelta(days=np.random.randint(30, 365))
                
                predictions.append({
                    "prediction_id": f"PRED_{policy['policy_number']}_{model['model_name'].replace(' ', '_')}_{i}_{j}",
                    "prediction_type": np.random.choice(prediction_types),
                    "target_policy_id": i + 1,
                    "target_jurisdiction": policy["jurisdiction"],
                    "target_industry": policy.get("affected_industries", [None])[0] if policy.get("affected_industries") else None,
                    "prediction_horizon": np.random.randint(3, 24),
                    "confidence_level": np.random.uniform(0.6, 0.95),
                    "scenario": np.random.choice(["baseline", "optimistic", "pessimistic"]),
                    "model_id": j + 1,
                    "model_version": model["model_version"],
                    "predicted_value": np.random.uniform(-100, 100),
                    "predicted_probability": np.random.uniform(0.1, 0.9),
                    "confidence_interval_lower": np.random.uniform(-150, 50),
                    "confidence_interval_upper": np.random.uniform(50, 150),
                    "prediction_date": prediction_date,
                    "target_date": target_date,
                    "status": "COMPLETED",
                    "prediction_notes": f"Prediction for {policy['title']} using {model['model_name']}"
                })
        
        return predictions 