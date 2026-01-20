"""Domain models for face detection service."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FaceDetectionResult:
    """Domain model representing the result of face detection."""

    face_detected: bool
    confidence: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {"face_detected": self.face_detected}
