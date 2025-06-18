"""
Policy data generator for synthetic policy data.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
from loguru import logger


class PolicyDataGenerator:
    """Generator for synthetic policy data."""
    
    def generate_categories(self) -> List[Dict[str, Any]]:
        """Generate synthetic policy categories."""
        categories = [
            {"name": "Trade Policy", "description": "International trade regulations and agreements"},
            {"name": "Financial Regulation", "description": "Banking and financial services regulations"},
            {"name": "Environmental Policy", "description": "Environmental protection and climate regulations"},
            {"name": "Tax Policy", "description": "Corporate and individual tax regulations"},
            {"name": "Labor Law", "description": "Employment and workplace regulations"},
            {"name": "Technology Regulation", "description": "Digital and technology sector regulations"},
            {"name": "Healthcare Policy", "description": "Healthcare and pharmaceutical regulations"},
            {"name": "Energy Policy", "description": "Energy sector regulations and incentives"},
            {"name": "Data Privacy", "description": "Data protection and privacy regulations"},
            {"name": "Antitrust", "description": "Competition and antitrust regulations"}
        ]
        
        return [{"id": i+1, **cat} for i, cat in enumerate(categories)]
    
    def generate_policies(self, num_policies: int, start_date: datetime, end_date: datetime, 
                         categories: List[Dict]) -> List[Dict[str, Any]]:
        """Generate synthetic policies."""
        policies = []
        
        policy_templates = [
            "Enhanced Capital Requirements for {industry}",
            "Environmental Compliance Standards for {industry}",
            "Data Protection Regulations for {industry}",
            "Trade Tariff Adjustments for {industry}",
            "Tax Incentive Program for {industry}",
            "Workplace Safety Standards for {industry}",
            "Supply Chain Transparency Requirements for {industry}",
            "Digital Transformation Mandates for {industry}",
            "Sustainability Reporting Requirements for {industry}",
            "Cybersecurity Standards for {industry}"
        ]
        
        jurisdictions = ["US", "EU", "UK", "JP", "CN", "CA", "AU", "IN", "BR", "MX"]
        industries = ["financial_services", "technology", "energy", "healthcare", "manufacturing"]
        policy_types = ["LEGISLATION", "REGULATION", "EXECUTIVE_ORDER", "GUIDANCE"]
        statuses = ["DRAFT", "PROPOSED", "ENACTED", "IMPLEMENTED"]
        
        for i in range(num_policies):
            jurisdiction = np.random.choice(jurisdictions)
            industry = np.random.choice(industries)
            category = np.random.choice(categories)
            
            # Generate dates
            proposed_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            enacted_date = proposed_date + timedelta(days=np.random.randint(30, 365)) if np.random.random() > 0.3 else None
            effective_date = enacted_date + timedelta(days=np.random.randint(0, 180)) if enacted_date else None
            
            policies.append({
                "id": i + 1,
                "title": np.random.choice(policy_templates).format(industry=industry.replace("_", " ").title()),
                "description": f"Comprehensive regulatory framework for {industry} sector",
                "policy_number": f"{jurisdiction}-{category['name'].replace(' ', '')[:3].upper()}-{i+1:04d}",
                "jurisdiction": jurisdiction,
                "policy_type": np.random.choice(policy_types),
                "status": np.random.choice(statuses),
                "proposed_date": proposed_date,
                "enacted_date": enacted_date,
                "effective_date": effective_date,
                "regulatory_body": f"{jurisdiction} Regulatory Authority",
                "estimated_impact": np.random.uniform(-500, 500),
                "impact_confidence": np.random.uniform(0.5, 0.9),
                "affected_industries": [industry],
                "category_id": category["id"]
            })
        
        return policies
    
    def generate_policy_changes(self, policies: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic policy changes."""
        changes = []
        
        change_types = ["amendment", "repeal", "extension", "modification", "clarification"]
        impact_directions = ["positive", "negative", "neutral"]
        
        for policy in policies:
            # Generate 1-3 changes per policy
            num_changes = np.random.randint(1, 4)
            
            for i in range(num_changes):
                change_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                
                changes.append({
                    "policy_id": policy["id"],
                    "change_type": np.random.choice(change_types),
                    "change_date": change_date,
                    "change_description": f"Modification to {policy['title']}",
                    "impact_magnitude": np.random.uniform(-1, 1),
                    "impact_direction": np.random.choice(impact_directions),
                    "source_document": f"Amendment-{policy['policy_number']}-{i+1}",
                    "legislative_session": f"Session-{change_date.year}"
                })
        
        return changes 