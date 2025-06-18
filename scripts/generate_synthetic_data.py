#!/usr/bin/env python3
"""
Script to generate synthetic data for PolicyRadar.
"""
import sys
import os
from datetime import datetime
import pandas as pd

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.synthetic.generator import SyntheticDataGenerator
from loguru import logger


def main():
    """Main function to generate synthetic data."""
    logger.info("Starting synthetic data generation...")
    
    # Initialize generator
    generator = SyntheticDataGenerator()
    
    # Generate data
    data = generator.generate_all_data(
        num_policies=1000,
        num_companies=500,
        num_market_records=10000,
        start_date=datetime(2015, 1, 1),
        end_date=datetime(2025, 12, 31)
    )
    
    # Save data
    generator.save_data(data, format="json")
    generator.save_data(data, format="csv")
    
    # Print summary
    logger.info("Data generation completed!")
    logger.info("Generated data summary:")
    for data_type, records in data.items():
        logger.info(f"  {data_type}: {len(records)} records")
    
    # Save summary to file
    summary = {
        "generation_date": datetime.now().isoformat(),
        "data_summary": {data_type: len(records) for data_type, records in data.items()},
        "total_records": sum(len(records) for records in data.values())
    }
    
    with open(os.path.join(generator.output_dir, "generation_summary.json"), "w") as f:
        import json
        json.dump(summary, f, indent=2)
    
    logger.info(f"Summary saved to {os.path.join(generator.output_dir, 'generation_summary.json')}")


if __name__ == "__main__":
    main() 