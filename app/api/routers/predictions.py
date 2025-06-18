"""
Predictions API router.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_predictions():
    """Get predictions."""
    return {"message": "Predictions endpoint"}


@router.get("/models")
async def get_prediction_models():
    """Get prediction models."""
    return {"message": "Prediction models endpoint"}


@router.post("/generate")
async def generate_prediction():
    """Generate a new prediction."""
    return {"message": "Prediction generation endpoint"} 