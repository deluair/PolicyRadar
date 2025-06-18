"""
Company data generator for synthetic company data.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
from loguru import logger


class CompanyDataGenerator:
    """Generator for synthetic company data."""
    
    def generate_companies(self, num_companies: int) -> List[Dict[str, Any]]:
        """Generate synthetic companies."""
        companies = []
        
        # Fortune 500 company names (synthetic)
        company_names = [
            "GlobalTech Solutions", "MegaBank International", "GreenEnergy Corp", "HealthCare Plus",
            "Manufacturing Dynamics", "Digital Innovations", "Financial Services Group", "Energy Solutions",
            "Pharmaceutical Research", "Technology Systems", "Industrial Manufacturing", "Consumer Goods Co",
            "Telecommunications Network", "Transportation Logistics", "Real Estate Holdings", "Utilities Corp",
            "Materials Processing", "Aerospace Defense", "Biotechnology Research", "Automotive Systems"
        ]
        
        industries = ["financial_services", "technology", "energy", "healthcare", "manufacturing"]
        countries = ["US", "EU", "UK", "JP", "CN", "CA", "AU", "IN", "BR", "MX"]
        
        for i in range(num_companies):
            industry = np.random.choice(industries)
            country = np.random.choice(countries)
            
            companies.append({
                "id": i + 1,
                "name": f"{np.random.choice(company_names)} {i+1}",
                "ticker_symbol": f"TICK{i+1:03d}",
                "industry": industry,
                "headquarters_country": country,
                "market_cap": np.random.uniform(1000, 50000),
                "revenue": np.random.uniform(500, 25000),
                "employees": np.random.randint(1000, 100000),
                "fortune_500_rank": np.random.randint(1, 500) if np.random.random() > 0.7 else None,
                "primary_markets": [country, np.random.choice(countries)],
                "regulatory_jurisdictions": [country, np.random.choice(countries)]
            })
        
        return companies
    
    def generate_company_profiles(self, companies: List[Dict]) -> List[Dict[str, Any]]:
        """Generate synthetic company profiles."""
        profiles = []
        
        esg_ratings = ["A", "B", "C", "D"]
        risk_tolerances = ["low", "medium", "high"]
        
        for company in companies:
            profiles.append({
                "company_id": company["id"],
                "description": f"Leading {company['industry'].replace('_', ' ')} company",
                "mission_statement": f"To provide innovative solutions in {company['industry'].replace('_', ' ')}",
                "vision_statement": f"To be the global leader in {company['industry'].replace('_', ' ')}",
                "ceo": f"CEO {company['id']}",
                "cfo": f"CFO {company['id']}",
                "general_counsel": f"GC {company['id']}",
                "website": f"https://www.{company['name'].lower().replace(' ', '')}.com",
                "esg_rating": np.random.choice(esg_ratings),
                "carbon_footprint": np.random.uniform(1000, 50000),
                "risk_tolerance": np.random.choice(risk_tolerances),
                "political_exposure": np.random.uniform(0.1, 0.9),
                "regulatory_risk_score": np.random.uniform(0.1, 0.9)
            })
        
        return profiles
    
    def generate_financial_metrics(self, companies: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic financial metrics."""
        metrics = []
        
        for company in companies:
            # Generate quarterly data for the date range
            current_date = start_date
            while current_date <= end_date:
                # Generate realistic financial data
                revenue = company["revenue"] * (1 + np.random.normal(0, 0.05))  # 5% quarterly variation
                net_income = revenue * np.random.uniform(0.05, 0.25)  # 5-25% profit margin
                operating_income = net_income * np.random.uniform(1.1, 1.5)
                ebitda = operating_income * np.random.uniform(1.05, 1.2)
                
                total_assets = revenue * np.random.uniform(1.5, 3.0)
                total_liabilities = total_assets * np.random.uniform(0.3, 0.7)
                shareholders_equity = total_assets - total_liabilities
                
                metrics.append({
                    "company_id": company["id"],
                    "date": current_date,
                    "total_revenue": revenue,
                    "revenue_growth": np.random.uniform(-0.1, 0.2),
                    "net_income": net_income,
                    "operating_income": operating_income,
                    "ebitda": ebitda,
                    "profit_margin": net_income / revenue,
                    "total_assets": total_assets,
                    "total_liabilities": total_liabilities,
                    "shareholders_equity": shareholders_equity,
                    "debt_to_equity": total_liabilities / shareholders_equity if shareholders_equity > 0 else 0,
                    "operating_cash_flow": operating_income * np.random.uniform(0.8, 1.2),
                    "free_cash_flow": operating_income * np.random.uniform(0.6, 1.0),
                    "market_cap": company["market_cap"] * (1 + np.random.normal(0, 0.1)),
                    "pe_ratio": np.random.uniform(10, 30),
                    "effective_tax_rate": np.random.uniform(0.15, 0.35),
                    "tax_expense": net_income * np.random.uniform(0.15, 0.35)
                })
                
                # Move to next quarter
                current_date += timedelta(days=90)
        
        return metrics 