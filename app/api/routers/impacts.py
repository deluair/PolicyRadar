"""
Impacts API router.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db

router = APIRouter()


@router.get("/")
async def get_impact_assessments(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get impact assessments."""
    return {"message": "Impact assessments endpoint"}


@router.get("/{assessment_id}")
async def get_impact_assessment(
    assessment_id: int = Path(...),
    db: Session = Depends(get_db)
):
    """Get a specific impact assessment."""
    return {"message": f"Impact assessment {assessment_id}"} 