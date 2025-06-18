"""
Prediction data models.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from .base import Base


class PredictionStatus(enum.Enum):
    """Prediction status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ModelType(enum.Enum):
    """Model type enumeration."""
    TIME_SERIES = "time_series"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    NLP = "nlp"
    ENSEMBLE = "ensemble"
    DEEP_LEARNING = "deep_learning"
    ECONOMETRIC = "econometric"


class PolicyPrediction(Base):
    """Policy prediction model."""
    __tablename__ = "policy_predictions"
    
    # Prediction details
    prediction_id = Column(String(100), unique=True, nullable=False, index=True)
    prediction_type = Column(String(100), nullable=False)  # policy_change, impact_forecast, etc.
    
    # Target policy
    target_policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True)
    target_jurisdiction = Column(String(10), nullable=False, index=True)
    target_industry = Column(String(100), nullable=True)
    
    # Prediction parameters
    prediction_horizon = Column(Integer, nullable=True)  # In months
    confidence_level = Column(Float, nullable=True)  # 0-1 confidence
    scenario = Column(String(100), nullable=True)  # baseline, optimistic, pessimistic
    
    # Model information
    model_id = Column(Integer, ForeignKey("prediction_models.id"), nullable=True)
    model_version = Column(String(50), nullable=True)
    features_used = Column(JSONB, nullable=True)  # List of features used
    
    # Prediction results
    predicted_value = Column(Float, nullable=True)
    predicted_probability = Column(Float, nullable=True)
    confidence_interval_lower = Column(Float, nullable=True)
    confidence_interval_upper = Column(Float, nullable=True)
    
    # Time information
    prediction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=True)  # When the prediction is for
    
    # Status and tracking
    status = Column(Enum(PredictionStatus), nullable=False, default=PredictionStatus.PENDING)
    actual_outcome = Column(Float, nullable=True)  # Actual result when available
    accuracy_score = Column(Float, nullable=True)  # How accurate the prediction was
    
    # Additional metadata
    prediction_notes = Column(Text, nullable=True)
    external_factors = Column(JSONB, nullable=True)  # External factors considered
    assumptions = Column(JSONB, nullable=True)  # Key assumptions made
    
    # Relationships
    model = relationship("PredictionModel", back_populates="predictions")


class PredictionModel(Base):
    """Prediction model metadata."""
    __tablename__ = "prediction_models"
    
    # Model identification
    model_name = Column(String(200), nullable=False, index=True)
    model_type = Column(Enum(ModelType), nullable=False)
    model_version = Column(String(50), nullable=False)
    
    # Model details
    description = Column(Text, nullable=True)
    algorithm = Column(String(100), nullable=True)  # XGBoost, LSTM, ARIMA, etc.
    hyperparameters = Column(JSONB, nullable=True)  # Model hyperparameters
    
    # Training information
    training_start_date = Column(DateTime, nullable=True)
    training_end_date = Column(DateTime, nullable=True)
    training_data_size = Column(Integer, nullable=True)
    training_features = Column(JSONB, nullable=True)  # List of training features
    
    # Performance metrics
    accuracy_score = Column(Float, nullable=True)
    precision_score = Column(Float, nullable=True)
    recall_score = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    mse = Column(Float, nullable=True)  # Mean squared error
    mae = Column(Float, nullable=True)  # Mean absolute error
    
    # Validation
    validation_method = Column(String(100), nullable=True)  # cross_validation, holdout, etc.
    validation_score = Column(Float, nullable=True)
    backtesting_results = Column(JSONB, nullable=True)  # Backtesting performance
    
    # Model files
    model_file_path = Column(String(500), nullable=True)
    feature_scaler_path = Column(String(500), nullable=True)
    preprocessing_pipeline_path = Column(String(500), nullable=True)
    
    # Deployment
    is_active = Column(Boolean, nullable=False, default=True)
    deployment_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    
    # Monitoring
    performance_monitoring = Column(JSONB, nullable=True)  # Monitoring configuration
    drift_detection = Column(JSONB, nullable=True)  # Drift detection settings
    retraining_schedule = Column(String(100), nullable=True)  # Retraining frequency
    
    # Relationships
    predictions = relationship("PolicyPrediction", back_populates="model")


# Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, List


class PolicyPredictionSchema(BaseModel):
    """Policy prediction schema."""
    id: Optional[int] = None
    prediction_id: str
    prediction_type: str
    
    target_policy_id: Optional[int] = None
    target_jurisdiction: str
    target_industry: Optional[str] = None
    
    prediction_horizon: Optional[int] = None
    confidence_level: Optional[float] = None
    scenario: Optional[str] = None
    
    model_id: Optional[int] = None
    model_version: Optional[str] = None
    features_used: Optional[List[str]] = None
    
    predicted_value: Optional[float] = None
    predicted_probability: Optional[float] = None
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    
    prediction_date: datetime
    target_date: Optional[datetime] = None
    
    status: PredictionStatus = PredictionStatus.PENDING
    actual_outcome: Optional[float] = None
    accuracy_score: Optional[float] = None
    
    prediction_notes: Optional[str] = None
    external_factors: Optional[List[str]] = None
    assumptions: Optional[dict] = None
    
    class Config:
        from_attributes = True


class PredictionModelSchema(BaseModel):
    """Prediction model schema."""
    id: Optional[int] = None
    model_name: str
    model_type: ModelType
    model_version: str
    
    description: Optional[str] = None
    algorithm: Optional[str] = None
    hyperparameters: Optional[dict] = None
    
    training_start_date: Optional[datetime] = None
    training_end_date: Optional[datetime] = None
    training_data_size: Optional[int] = None
    training_features: Optional[List[str]] = None
    
    accuracy_score: Optional[float] = None
    precision_score: Optional[float] = None
    recall_score: Optional[float] = None
    f1_score: Optional[float] = None
    mse: Optional[float] = None
    mae: Optional[float] = None
    
    validation_method: Optional[str] = None
    validation_score: Optional[float] = None
    backtesting_results: Optional[dict] = None
    
    model_file_path: Optional[str] = None
    feature_scaler_path: Optional[str] = None
    preprocessing_pipeline_path: Optional[str] = None
    
    is_active: bool = True
    deployment_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    performance_monitoring: Optional[dict] = None
    drift_detection: Optional[dict] = None
    retraining_schedule: Optional[str] = None
    
    class Config:
        from_attributes = True 