"""
Basic tests for PolicyRadar.
"""
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that all modules can be imported."""
    try:
        from config.settings import settings
        assert settings.app_name == "PolicyRadar"
    except ImportError as e:
        pytest.fail(f"Failed to import settings: {e}")


def test_synthetic_data_generation():
    """Test synthetic data generation."""
    try:
        from data.synthetic.generator import SyntheticDataGenerator
        generator = SyntheticDataGenerator()
        assert generator is not None
    except ImportError as e:
        pytest.fail(f"Failed to import SyntheticDataGenerator: {e}")


def test_policy_data_generator():
    """Test policy data generator."""
    try:
        from data.synthetic.policy_data import PolicyDataGenerator
        generator = PolicyDataGenerator()
        categories = generator.generate_categories()
        assert len(categories) > 0
    except ImportError as e:
        pytest.fail(f"Failed to import PolicyDataGenerator: {e}")


def test_company_data_generator():
    """Test company data generator."""
    try:
        from data.synthetic.company_data import CompanyDataGenerator
        generator = CompanyDataGenerator()
        companies = generator.generate_companies(5)
        assert len(companies) == 5
    except ImportError as e:
        pytest.fail(f"Failed to import CompanyDataGenerator: {e}")


if __name__ == "__main__":
    pytest.main([__file__]) 