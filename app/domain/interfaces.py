"""Domain interfaces for face detection service."""

from abc import ABC, abstractmethod

from app.domain.models import FaceDetectionResult


class IFaceDetector(ABC):
    """Interface for face detection implementations."""

    @abstractmethod
    def detect_face(self, image_data: bytes) -> FaceDetectionResult:
        """
        Detect faces in the provided image data.

        Args:
            image_data: Raw image bytes

        Returns:
            FaceDetectionResult containing detection status

        Raises:
            ValueError: If image data is invalid
        """
        pass
