"""
Market data generator for synthetic market data.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
from loguru import logger


class MarketDataGenerator:
    """Generator for synthetic market data."""
    
    def generate_market_data(self, num_records: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic market data."""
        market_data = []
        
        symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "JPM", "BAC", "WMT", "JNJ", "PG"]
        
        for i in range(num_records):
            date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            symbol = np.random.choice(symbols)
            
            # Generate realistic price data
            base_price = np.random.uniform(50, 500)
            daily_return = np.random.normal(0, 0.02)  # 2% daily volatility
            
            market_data.append({
                "id": i + 1,
                "symbol": symbol,
                "asset_type": "stock",
                "exchange": "NASDAQ" if symbol in ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"] else "NYSE",
                "date": date,
                "open_price": base_price,
                "high_price": base_price * (1 + abs(daily_return)),
                "low_price": base_price * (1 - abs(daily_return)),
                "close_price": base_price * (1 + daily_return),
                "volume": np.random.randint(1000000, 10000000),
                "daily_return": daily_return,
                "market_cap": np.random.uniform(1000, 50000)
            })
        
        return market_data
    
    def generate_economic_indicators(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic economic indicators."""
        indicators = []
        
        indicator_data = [
            {"name": "GDP Growth Rate", "code": "GDP_GROWTH", "category": "GDP", "unit": "percentage"},
            {"name": "Inflation Rate", "code": "INFLATION", "category": "inflation", "unit": "percentage"},
            {"name": "Unemployment Rate", "code": "UNEMPLOYMENT", "category": "employment", "unit": "percentage"},
            {"name": "Interest Rate", "code": "INTEREST_RATE", "category": "monetary", "unit": "percentage"},
            {"name": "Consumer Price Index", "code": "CPI", "category": "inflation", "unit": "index"}
        ]
        
        countries = ["US", "EU", "UK", "JP", "CN"]
        
        for country in countries:
            for indicator in indicator_data:
                for year in range(start_date.year, end_date.year + 1):
                    for quarter in range(1, 5):
                        date = datetime(year, quarter * 3, 1)
                        if start_date <= date <= end_date:
                            indicators.append({
                                "indicator_name": indicator["name"],
                                "indicator_code": f"{indicator['code']}_{country}",
                                "category": indicator["category"],
                                "country": country,
                                "date": date,
                                "frequency": "quarterly",
                                "value": np.random.uniform(0, 10) if "rate" in indicator["name"].lower() else np.random.uniform(100, 300),
                                "unit": indicator["unit"],
                                "source_agency": f"{country} Bureau of Statistics"
                            })
        
        return indicators
    
    def generate_trade_flows(self, companies: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate synthetic trade flows."""
        trade_flows = []
        
        countries = ["US", "EU", "UK", "JP", "CN", "CA", "AU", "IN", "BR", "MX"]
        product_categories = ["electronics", "automotive", "pharmaceuticals", "energy", "agriculture", "textiles"]
        transport_modes = ["sea", "air", "land", "rail"]
        
        for i in range(len(companies) * 10):  # Generate 10 trade flows per company
            company = np.random.choice(companies)
            origin = company["headquarters_country"]
            destination = np.random.choice([c for c in countries if c != origin])
            
            date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            
            trade_flows.append({
                "id": i + 1,
                "trade_id": f"TRADE_{i+1:06d}",
                "trade_type": np.random.choice(["import", "export"]),
                "origin_country": origin,
                "destination_country": destination,
                "product_category": np.random.choice(product_categories),
                "date": date,
                "quantity": np.random.uniform(100, 10000),
                "value_usd": np.random.uniform(10000, 1000000),
                "tariff_rate": np.random.uniform(0, 0.25),
                "duty_amount": np.random.uniform(0, 50000),
                "transport_mode": np.random.choice(transport_modes),
                "transit_time_days": np.random.randint(1, 30),
                "exporter_company": company["name"] if np.random.random() > 0.5 else None,
                "importer_company": company["name"] if np.random.random() > 0.5 else None,
                "data_source": "Customs Authority"
            })
        
        return trade_flows 