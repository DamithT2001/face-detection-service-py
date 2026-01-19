"""Dependency injection for API layer."""
from functools import lru_cache

from app.application.face_detection_service import FaceDetectionService
from app.infrastructure.mediapipe_detector import MediaPipeFaceDetector
from app.api.config import get_settings


@lru_cache()
def get_face_detector() -> MediaPipeFaceDetector:
    """
    Get or create MediaPipe face detector instance (cached).
    
    Returns:
        MediaPipeFaceDetector instance
    """
    settings = get_settings()
    return MediaPipeFaceDetector(
        min_detection_confidence=settings.min_detection_confidence
    )


def get_face_detection_service() -> FaceDetectionService:
    """
    Get face detection service instance with dependencies.
    
    Returns:
        FaceDetectionService instance
    """
    detector = get_face_detector()
    return FaceDetectionService(face_detector=detector)
