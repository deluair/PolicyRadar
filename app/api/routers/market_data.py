"""
Market data API router.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_market_data():
    """Get market data."""
    return {"message": "Market data endpoint"}


@router.get("/economic-indicators")
async def get_economic_indicators():
    """Get economic indicators."""
    return {"message": "Economic indicators endpoint"}


@router.get("/trade-flows")
async def get_trade_flows():
    """Get trade flows."""
    return {"message": "Trade flows endpoint"} 