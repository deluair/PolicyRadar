"""
Main FastAPI application for PolicyRadar.
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime, timedelta

from config.settings import settings
from app.api.routers import policies, companies, impacts, market_data, predictions, analytics
from app.core.database import get_db, engine
from data.models.base import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Comprehensive economic policy impact assessment system for Fortune 500 corporations",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(policies.router, prefix="/api/v1/policies", tags=["policies"])
app.include_router(companies.router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(impacts.router, prefix="/api/v1/impacts", tags=["impacts"])
app.include_router(market_data.router, prefix="/api/v1/market", tags=["market_data"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["predictions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PolicyRadar API",
        "version": settings.app_version,
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.app_version
    }


@app.get("/api/v1/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard summary data."""
    try:
        # This would typically fetch from database
        # For now, return synthetic summary data
        return {
            "total_policies": 1250,
            "active_policies": 890,
            "high_risk_policies": 45,
            "total_companies": 500,
            "affected_companies": 320,
            "total_impact_assessments": 2800,
            "average_impact": -15.5,
            "prediction_accuracy": 0.82,
            "recent_alerts": [
                {
                    "id": 1,
                    "type": "policy_change",
                    "title": "Basel III Implementation Update",
                    "severity": "high",
                    "timestamp": datetime.utcnow() - timedelta(hours=2)
                },
                {
                    "id": 2,
                    "type": "impact_alert",
                    "title": "Trade Tariff Impact on Manufacturing",
                    "severity": "medium",
                    "timestamp": datetime.utcnow() - timedelta(hours=6)
                }
            ],
            "risk_distribution": {
                "low": 45,
                "medium": 35,
                "high": 15,
                "critical": 5
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard summary: {str(e)}")


@app.get("/api/v1/analytics/trends")
async def get_analytics_trends(
    start_date: Optional[datetime] = Query(None, description="Start date for trend analysis"),
    end_date: Optional[datetime] = Query(None, description="End date for trend analysis"),
    jurisdiction: Optional[str] = Query(None, description="Jurisdiction filter"),
    industry: Optional[str] = Query(None, description="Industry filter")
):
    """Get analytics trends data."""
    try:
        # This would typically fetch from database and perform analysis
        # For now, return synthetic trend data
        return {
            "policy_trends": {
                "total_policies": [1200, 1250, 1300, 1350, 1400],
                "enacted_policies": [800, 850, 900, 950, 1000],
                "proposed_policies": [400, 400, 400, 400, 400],
                "dates": [
                    "2024-01", "2024-02", "2024-03", "2024-04", "2024-05"
                ]
            },
            "impact_trends": {
                "average_impact": [-10, -12, -15, -18, -20],
                "positive_impacts": [30, 25, 20, 15, 10],
                "negative_impacts": [70, 75, 80, 85, 90],
                "dates": [
                    "2024-01", "2024-02", "2024-03", "2024-04", "2024-05"
                ]
            },
            "risk_trends": {
                "high_risk_policies": [40, 42, 45, 48, 50],
                "critical_risk_policies": [5, 6, 7, 8, 9],
                "dates": [
                    "2024-01", "2024-02", "2024-03", "2024-04", "2024-05"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics trends: {str(e)}")


@app.get("/api/v1/reports/generate")
async def generate_report(
    report_type: str = Query(..., description="Type of report to generate"),
    company_id: Optional[int] = Query(None, description="Company ID for company-specific reports"),
    policy_id: Optional[int] = Query(None, description="Policy ID for policy-specific reports"),
    format: str = Query("pdf", description="Report format (pdf, excel, json)")
):
    """Generate reports."""
    try:
        # This would typically generate actual reports
        # For now, return report metadata
        return {
            "report_id": f"REP_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "report_type": report_type,
            "company_id": company_id,
            "policy_id": policy_id,
            "format": format,
            "status": "generated",
            "download_url": f"/api/v1/reports/download/REP_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "app.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    ) 