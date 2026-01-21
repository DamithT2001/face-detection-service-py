"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image

from app.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def create_test_image(width=100, height=100, format="PNG") -> BytesIO:
    """Create a test image file."""
    image = Image.new("RGB", (width, height), color=(73, 109, 137))
    buffer = BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestFaceDetectionEndpoint:
    """Test cases for face detection endpoint."""

    def test_detect_face_with_valid_image(self, client):
        """Test face detection with valid image."""
        # Arrange
        image_file = create_test_image()

        # Act
        response = client.post(
            "/api/detect-face", files={"file": ("test.png", image_file, "image/png")}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "face_detected" in data
        assert isinstance(data["face_detected"], bool)

    def test_detect_face_without_file(self, client):
        """Test face detection without file."""
        # Act
        response = client.post("/api/detect-face")

        # Assert
        assert response.status_code == 422  # Validation error

    def test_detect_face_with_empty_file(self, client):
        """Test face detection with empty file."""
        # Arrange
        empty_file = BytesIO(b"")

        # Act
        response = client.post(
            "/api/detect-face", files={"file": ("empty.png", empty_file, "image/png")}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_detect_face_with_invalid_file_type(self, client):
        """Test face detection with non-image file."""
        # Arrange
        text_file = BytesIO(b"This is not an image")

        # Act
        response = client.post(
            "/api/detect-face", files={"file": ("test.txt", text_file, "text/plain")}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "Invalid file type" in data["detail"]

    def test_detect_face_with_corrupted_image(self, client):
        """Test face detection with corrupted image data."""
        # Arrange
        corrupted_data = BytesIO(b"corrupted_image_data")

        # Act
        response = client.post(
            "/api/detect-face",
            files={"file": ("corrupted.png", corrupted_data, "image/png")},
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_detect_face_response_schema(self, client):
        """Test that response matches expected schema."""
        # Arrange
        image_file = create_test_image()

        # Act
        response = client.post(
            "/api/detect-face", files={"file": ("test.png", image_file, "image/png")}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        # Verify only face_detected is in response (no confidence or other fields)
        assert set(data.keys()) == {"face_detected"}


class TestAPIDocumentation:
    """Test cases for API documentation."""

    def test_openapi_json_available(self, client):
        """Test OpenAPI JSON is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_swagger_docs_available(self, client):
        """Test Swagger UI is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Test ReDoc is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
