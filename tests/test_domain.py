"""Tests for domain models."""
import pytest

from app.domain.models import FaceDetectionResult


class TestFaceDetectionResult:
    """Test cases for FaceDetectionResult domain model."""
    
    def test_create_result_with_face_detected(self):
        """Test creating result with face detected."""
        result = FaceDetectionResult(face_detected=True, confidence=0.95)
        
        assert result.face_detected is True
        assert result.confidence == 0.95
    
    def test_create_result_without_face(self):
        """Test creating result without face detected."""
        result = FaceDetectionResult(face_detected=False)
        
        assert result.face_detected is False
        assert result.confidence is None
    
    def test_to_dict(self):
        """Test converting result to dictionary."""
        result = FaceDetectionResult(face_detected=True, confidence=0.85)
        result_dict = result.to_dict()
        
        assert result_dict == {"face_detected": True}
        assert "confidence" not in result_dict
    
    def test_immutability(self):
        """Test that FaceDetectionResult is immutable."""
        result = FaceDetectionResult(face_detected=True)
        
        with pytest.raises(Exception):
            result.face_detected = False
