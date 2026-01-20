"""API request and response models."""
from pydantic import BaseModel, Field


class FaceDetectionResponse(BaseModel):
    """Response model for face detection endpoint."""

    face_detected: bool = Field(
        ...,
        description="Whether a human face was detected in the image"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "face_detected": True
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for error cases."""

    detail: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid image format"
            }
        }
