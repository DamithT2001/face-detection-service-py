"""Configuration management for the API."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_title: str = "Human Face Detection API"
    api_version: str = "1.0.0"
    api_description: str = (
        "Production-ready REST API for detecting human faces in images using MediaPipe"
    )
    
    # Server Configuration
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    
    # Face Detection Configuration
    min_detection_confidence: float = 0.5
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()
