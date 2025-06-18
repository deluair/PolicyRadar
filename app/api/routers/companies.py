"""
Companies API router.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from data.models.company import Company, CompanyProfile, FinancialMetrics
from data.models.company import CompanySchema, CompanyProfileSchema, FinancialMetricsSchema

router = APIRouter()


@router.get("/", response_model=List[CompanySchema])
async def get_companies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    industry: Optional[str] = Query(None),
    country: Optional[str] = Query(None)
):
    """Get companies with filtering and pagination."""
    try:
        query = db.query(Company)
        
        if industry:
            query = query.filter(Company.industry == industry)
        if country:
            query = query.filter(Company.headquarters_country == country)
        
        companies = query.offset(skip).limit(limit).all()
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")


@router.get("/{company_id}", response_model=CompanySchema)
async def get_company(
    company_id: int = Path(...),
    db: Session = Depends(get_db)
):
    """Get a specific company by ID."""
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company: {str(e)}")


@router.get("/{company_id}/profile", response_model=CompanyProfileSchema)
async def get_company_profile(
    company_id: int = Path(...),
    db: Session = Depends(get_db)
):
    """Get company profile."""
    try:
        profile = db.query(CompanyProfile).filter(CompanyProfile.company_id == company_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Company profile not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company profile: {str(e)}")


@router.get("/{company_id}/financial-metrics", response_model=List[FinancialMetricsSchema])
async def get_company_financial_metrics(
    company_id: int = Path(...),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get company financial metrics."""
    try:
        metrics = db.query(FinancialMetrics).filter(
            FinancialMetrics.company_id == company_id
        ).order_by(FinancialMetrics.date.desc()).offset(skip).limit(limit).all()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching financial metrics: {str(e)}") 