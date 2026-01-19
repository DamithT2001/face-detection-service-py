"""Tests for face detection service."""
import pytest
from unittest.mock import Mock

from app.application.face_detection_service import FaceDetectionService
from app.domain.models import FaceDetectionResult
from app.domain.interfaces import IFaceDetector


class TestFaceDetectionService:
    """Test cases for FaceDetectionService."""
    
    @pytest.fixture
    def mock_detector(self):
        """Create mock face detector."""
        return Mock(spec=IFaceDetector)
    
    @pytest.fixture
    def service(self, mock_detector):
        """Create service with mock detector."""
        return FaceDetectionService(face_detector=mock_detector)
    
    def test_detect_face_success(self, service, mock_detector):
        """Test successful face detection."""
        # Arrange
        image_data = b"fake_image_data"
        expected_result = FaceDetectionResult(face_detected=True, confidence=0.9)
        mock_detector.detect_face.return_value = expected_result
        
        # Act
        result = service.detect_face_in_image(image_data)
        
        # Assert
        assert result.face_detected is True
        assert result.confidence == 0.9
        mock_detector.detect_face.assert_called_once_with(image_data)
    
    def test_detect_no_face(self, service, mock_detector):
        """Test when no face is detected."""
        # Arrange
        image_data = b"fake_image_data"
        expected_result = FaceDetectionResult(face_detected=False)
        mock_detector.detect_face.return_value = expected_result
        
        # Act
        result = service.detect_face_in_image(image_data)
        
        # Assert
        assert result.face_detected is False
        assert result.confidence is None
        mock_detector.detect_face.assert_called_once_with(image_data)
    
    def test_detect_face_with_empty_data(self, service, mock_detector):
        """Test that empty image data raises ValueError."""
        # Arrange
        image_data = b""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Image data cannot be empty"):
            service.detect_face_in_image(image_data)
        
        mock_detector.detect_face.assert_not_called()
    
    def test_detect_face_propagates_detector_error(self, service, mock_detector):
        """Test that detector errors are propagated."""
        # Arrange
        image_data = b"fake_image_data"
        mock_detector.detect_face.side_effect = ValueError("Invalid image format")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid image format"):
            service.detect_face_in_image(image_data)
