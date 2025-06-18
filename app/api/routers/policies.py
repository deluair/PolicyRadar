"""
Policies API router.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from data.models.policy import Policy, PolicyCategory, PolicyChange
from data.models.policy import PolicySchema, PolicyCategorySchema, PolicyChangeSchema

router = APIRouter()


@router.get("/", response_model=List[PolicySchema])
async def get_policies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
    industry: Optional[str] = Query(None, description="Filter by affected industry"),
    status: Optional[str] = Query(None, description="Filter by policy status"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date")
):
    """Get policies with filtering and pagination."""
    try:
        query = db.query(Policy)
        
        # Apply filters
        if jurisdiction:
            query = query.filter(Policy.jurisdiction == jurisdiction)
        if industry:
            query = query.filter(Policy.affected_industries.contains([industry]))
        if status:
            query = query.filter(Policy.status == status)
        if category_id:
            query = query.filter(Policy.category_id == category_id)
        if start_date:
            query = query.filter(Policy.proposed_date >= start_date)
        if end_date:
            query = query.filter(Policy.proposed_date <= end_date)
        
        # Apply pagination
        policies = query.offset(skip).limit(limit).all()
        
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching policies: {str(e)}")


@router.get("/{policy_id}", response_model=PolicySchema)
async def get_policy(
    policy_id: int = Path(..., description="Policy ID"),
    db: Session = Depends(get_db)
):
    """Get a specific policy by ID."""
    try:
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching policy: {str(e)}")


@router.post("/", response_model=PolicySchema)
async def create_policy(
    policy: PolicySchema,
    db: Session = Depends(get_db)
):
    """Create a new policy."""
    try:
        db_policy = Policy(**policy.dict(exclude={"id"}))
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        return db_policy
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating policy: {str(e)}")


@router.put("/{policy_id}", response_model=PolicySchema)
async def update_policy(
    policy_id: int = Path(..., description="Policy ID"),
    policy: PolicySchema = None,
    db: Session = Depends(get_db)
):
    """Update an existing policy."""
    try:
        db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not db_policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        for key, value in policy.dict(exclude={"id"}).items():
            setattr(db_policy, key, value)
        
        db.commit()
        db.refresh(db_policy)
        return db_policy
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating policy: {str(e)}")


@router.delete("/{policy_id}")
async def delete_policy(
    policy_id: int = Path(..., description="Policy ID"),
    db: Session = Depends(get_db)
):
    """Delete a policy."""
    try:
        db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not db_policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        db.delete(db_policy)
        db.commit()
        return {"message": "Policy deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting policy: {str(e)}")


@router.get("/{policy_id}/changes", response_model=List[PolicyChangeSchema])
async def get_policy_changes(
    policy_id: int = Path(..., description="Policy ID"),
    db: Session = Depends(get_db)
):
    """Get changes for a specific policy."""
    try:
        changes = db.query(PolicyChange).filter(PolicyChange.policy_id == policy_id).all()
        return changes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching policy changes: {str(e)}")


@router.get("/categories/", response_model=List[PolicyCategorySchema])
async def get_policy_categories(
    db: Session = Depends(get_db)
):
    """Get all policy categories."""
    try:
        categories = db.query(PolicyCategory).all()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching policy categories: {str(e)}")


@router.get("/analytics/summary")
async def get_policy_analytics_summary(
    db: Session = Depends(get_db),
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
    start_date: Optional[datetime] = Query(None, description="Start date for analysis"),
    end_date: Optional[datetime] = Query(None, description="End date for analysis")
):
    """Get policy analytics summary."""
    try:
        query = db.query(Policy)
        
        if jurisdiction:
            query = query.filter(Policy.jurisdiction == jurisdiction)
        if start_date:
            query = query.filter(Policy.proposed_date >= start_date)
        if end_date:
            query = query.filter(Policy.proposed_date <= end_date)
        
        policies = query.all()
        
        # Calculate summary statistics
        total_policies = len(policies)
        enacted_policies = len([p for p in policies if p.status == "ENACTED"])
        proposed_policies = len([p for p in policies if p.status == "PROPOSED"])
        
        # Calculate average impact
        impacts = [p.estimated_impact for p in policies if p.estimated_impact is not None]
        average_impact = sum(impacts) / len(impacts) if impacts else 0
        
        # Jurisdiction breakdown
        jurisdiction_counts = {}
        for policy in policies:
            jurisdiction_counts[policy.jurisdiction] = jurisdiction_counts.get(policy.jurisdiction, 0) + 1
        
        # Industry breakdown
        industry_counts = {}
        for policy in policies:
            if policy.affected_industries:
                for industry in policy.affected_industries:
                    industry_counts[industry] = industry_counts.get(industry, 0) + 1
        
        return {
            "total_policies": total_policies,
            "enacted_policies": enacted_policies,
            "proposed_policies": proposed_policies,
            "average_impact": average_impact,
            "jurisdiction_breakdown": jurisdiction_counts,
            "industry_breakdown": industry_counts,
            "analysis_period": {
                "start_date": start_date,
                "end_date": end_date
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating policy analytics: {str(e)}")


@router.get("/search/")
async def search_policies(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Search policies by title, description, or content."""
    try:
        # Simple text search - in production, use full-text search
        query = db.query(Policy).filter(
            (Policy.title.ilike(f"%{q}%")) |
            (Policy.description.ilike(f"%{q}%")) |
            (Policy.content_summary.ilike(f"%{q}%"))
        )
        
        policies = query.offset(skip).limit(limit).all()
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching policies: {str(e)}")


@router.get("/recent/", response_model=List[PolicySchema])
async def get_recent_policies(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500)
):
    """Get recently proposed or enacted policies."""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        policies = db.query(Policy).filter(
            Policy.proposed_date >= cutoff_date
        ).order_by(Policy.proposed_date.desc()).limit(limit).all()
        
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent policies: {str(e)}")


@router.get("/high-risk/", response_model=List[PolicySchema])
async def get_high_risk_policies(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500)
):
    """Get policies with high estimated impact."""
    try:
        # Get policies with high negative impact or low confidence
        policies = db.query(Policy).filter(
            (Policy.estimated_impact < -100) |  # High negative impact
            (Policy.impact_confidence < 0.6)    # Low confidence
        ).order_by(Policy.estimated_impact.asc()).limit(limit).all()
        
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching high-risk policies: {str(e)}") 