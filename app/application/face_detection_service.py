"""Application service for face detection use cases."""
import logging
from typing import Optional

from app.domain.interfaces import IFaceDetector
from app.domain.models import FaceDetectionResult


logger = logging.getLogger(__name__)


class FaceDetectionService:
    """Service for handling face detection use cases."""
    
    def __init__(self, face_detector: IFaceDetector):
        """
        Initialize the face detection service.
        
        Args:
            face_detector: Implementation of face detector interface
        """
        self._face_detector = face_detector
    
    def detect_face_in_image(self, image_data: bytes) -> FaceDetectionResult:
        """
        Execute face detection on provided image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            FaceDetectionResult with detection status
            
        Raises:
            ValueError: If image data is invalid or empty
        """
        if not image_data:
            logger.warning("Empty image data provided")
            raise ValueError("Image data cannot be empty")
        
        try:
            logger.info("Processing face detection request")
            result = self._face_detector.detect_face(image_data)
            logger.info(f"Face detection completed: face_detected={result.face_detected}")
            return result
        except Exception as e:
            logger.error(f"Face detection failed: {str(e)}")
            raise
