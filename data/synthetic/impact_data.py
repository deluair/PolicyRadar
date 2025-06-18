"""
Impact data generator for synthetic impact assessment data.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
from loguru import logger


class ImpactDataGenerator:
    """Generator for synthetic impact assessment data."""
    
    def generate_impact_assessments(self, policies: List[Dict], companies: List[Dict], 
                                  start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic impact assessments."""
        assessments = []
        
        impact_directions = ["POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"]
        risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        scenarios = ["baseline", "optimistic", "pessimistic"]
        
        for i, policy in enumerate(policies):
            # Select companies that might be affected by this policy
            affected_companies = [c for c in companies if c["industry"] in policy.get("affected_industries", [])]
            
            if not affected_companies:
                continue
                
            for company in affected_companies[:5]:  # Limit to 5 companies per policy
                assessment_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
                
                assessments.append({
                    "id": len(assessments) + 1,
                    "policy_id": policy["id"],
                    "company_id": company["id"],
                    "assessment_date": assessment_date,
                    "assessment_period": f"{assessment_date.year}-{assessment_date.year + 1}",
                    "scenario": np.random.choice(scenarios),
                    "overall_impact": np.random.uniform(-200, 200),
                    "impact_direction": np.random.choice(impact_directions),
                    "confidence_level": np.random.uniform(0.6, 0.9),
                    "revenue_impact": np.random.uniform(-100, 100),
                    "cost_impact": np.random.uniform(-50, 50),
                    "capital_impact": np.random.uniform(-30, 30),
                    "tax_impact": np.random.uniform(-20, 20),
                    "risk_level": np.random.choice(risk_levels),
                    "risk_score": np.random.uniform(0.1, 0.9),
                    "implementation_date": assessment_date + timedelta(days=np.random.randint(30, 365)),
                    "compliance_deadline": assessment_date + timedelta(days=np.random.randint(60, 730)),
                    "mitigation_cost": np.random.uniform(1, 20),
                    "mitigation_effectiveness": np.random.uniform(0.3, 0.8)
                })
        
        return assessments
    
    def generate_impact_metrics(self, assessments: List[Dict]) -> List[Dict[str, Any]]:
        """Generate synthetic impact metrics."""
        metrics = []
        
        metric_categories = ["financial", "operational", "strategic"]
        metric_names = [
            "Revenue Impact", "Cost Impact", "Capital Requirements", "Tax Impact",
            "Market Share", "Customer Satisfaction", "Employee Productivity",
            "Supply Chain Efficiency", "Regulatory Compliance", "Innovation Pipeline"
        ]
        
        for assessment in assessments:
            # Generate 3-5 metrics per assessment
            num_metrics = np.random.randint(3, 6)
            selected_metrics = np.random.choice(metric_names, num_metrics, replace=False)
            
            for metric_name in selected_metrics:
                baseline_value = np.random.uniform(100, 1000)
                projected_value = baseline_value * (1 + np.random.uniform(-0.3, 0.3))
                change_amount = projected_value - baseline_value
                change_percentage = (change_amount / baseline_value) * 100
                
                metrics.append({
                    "assessment_id": assessment["id"],
                    "metric_name": metric_name,
                    "metric_category": np.random.choice(metric_categories),
                    "metric_unit": "USD millions" if "Impact" in metric_name else "percentage",
                    "baseline_value": baseline_value,
                    "projected_value": projected_value,
                    "change_amount": change_amount,
                    "change_percentage": change_percentage,
                    "time_period": f"Q{np.random.randint(1, 5)} {assessment['assessment_date'].year}",
                    "confidence_interval_lower": projected_value * 0.8,
                    "confidence_interval_upper": projected_value * 1.2
                })
        
        return metrics
    
    def generate_risk_scores(self, assessments: List[Dict]) -> List[Dict[str, Any]]:
        """Generate synthetic risk scores."""
        risk_scores = []
        
        risk_categories = ["regulatory", "operational", "financial", "strategic", "reputational"]
        risk_factors = [
            "Policy Implementation Delay", "Compliance Cost Overrun", "Market Reaction",
            "Supply Chain Disruption", "Regulatory Enforcement", "Competitive Response",
            "Technology Integration", "Employee Resistance", "Customer Backlash",
            "Legal Challenges", "Political Opposition", "Economic Downturn"
        ]
        
        for assessment in assessments:
            # Generate 2-4 risk scores per assessment
            num_risks = np.random.randint(2, 5)
            selected_categories = np.random.choice(risk_categories, num_risks, replace=False)
            
            for category in selected_categories:
                probability_score = np.random.uniform(0.1, 0.9)
                severity_score = np.random.uniform(0.1, 0.9)
                overall_risk_score = probability_score * severity_score
                
                # Determine risk level based on overall score
                if overall_risk_score < 0.25:
                    risk_level = "LOW"
                elif overall_risk_score < 0.5:
                    risk_level = "MEDIUM"
                elif overall_risk_score < 0.75:
                    risk_level = "HIGH"
                else:
                    risk_level = "CRITICAL"
                
                risk_scores.append({
                    "assessment_id": assessment["id"],
                    "risk_category": category,
                    "risk_factor": np.random.choice(risk_factors),
                    "risk_description": f"Risk related to {category} in policy implementation",
                    "probability_score": probability_score,
                    "severity_score": severity_score,
                    "overall_risk_score": overall_risk_score,
                    "risk_level": risk_level,
                    "mitigation_measures": [
                        "Enhanced monitoring",
                        "Contingency planning",
                        "Stakeholder engagement"
                    ],
                    "residual_risk_score": overall_risk_score * np.random.uniform(0.3, 0.7),
                    "monitoring_frequency": np.random.choice(["daily", "weekly", "monthly"]),
                    "trigger_conditions": {
                        "threshold": overall_risk_score * 1.2,
                        "timeframe": "30 days"
                    }
                })
        
        return risk_scores 