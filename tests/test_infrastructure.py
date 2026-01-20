"""Tests for MediaPipe face detector."""
import pytest
import numpy as np
from PIL import Image
from io import BytesIO

from app.infrastructure.mediapipe_detector import MediaPipeFaceDetector
from app.domain.models import FaceDetectionResult


class TestMediaPipeFaceDetector:
    """Test cases for MediaPipeFaceDetector."""
    
    @pytest.fixture
    def detector(self):
        """Create detector instance."""
        return MediaPipeFaceDetector(min_detection_confidence=0.5)
    
    def _create_test_image(self, width=100, height=100, color=(255, 0, 0)) -> bytes:
        """Create a simple test image."""
        image = Image.new('RGB', (width, height), color)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def test_detector_initialization(self, detector):
        """Test detector is properly initialized."""
        assert detector._min_detection_confidence == 0.5
        assert detector._mp_face_detection is not None
    
    def test_detect_with_valid_image(self, detector):
        """Test detection with valid image data."""
        # Create a simple test image
        image_data = self._create_test_image()
        
        # Act
        result = detector.detect_face(image_data)
        
        # Assert
        assert isinstance(result, FaceDetectionResult)
        assert isinstance(result.face_detected, bool)
    
    def test_detect_with_invalid_image_data(self, detector):
        """Test detection with invalid image data."""
        # Arrange
        invalid_data = b"not_an_image"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid image data"):
            detector.detect_face(invalid_data)
    
    def test_detect_with_empty_data(self, detector):
        """Test detection with empty data."""
        # Arrange
        empty_data = b""
        
        # Act & Assert
        with pytest.raises(ValueError):
            detector.detect_face(empty_data)
    
    def test_bytes_to_image_conversion(self, detector):
        """Test image bytes to numpy array conversion."""
        # Arrange
        image_data = self._create_test_image(width=50, height=50)
        
        # Act
        image_array = detector._bytes_to_image(image_data)
        
        # Assert
        assert isinstance(image_array, np.ndarray)
        assert len(image_array.shape) == 3  # Height, Width, Channels
        assert image_array.shape[2] == 3  # RGB channels
    
    def test_different_confidence_thresholds(self):
        """Test detector with different confidence thresholds."""
        detector_low = MediaPipeFaceDetector(min_detection_confidence=0.3)
        detector_high = MediaPipeFaceDetector(min_detection_confidence=0.9)
        
        assert detector_low._min_detection_confidence == 0.3
        assert detector_high._min_detection_confidence == 0.9
