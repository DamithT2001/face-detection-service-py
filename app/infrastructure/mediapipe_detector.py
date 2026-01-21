"""MediaPipe face detector implementation."""

import logging
from io import BytesIO

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

from app.domain.interfaces import IFaceDetector
from app.domain.models import FaceDetectionResult


logger = logging.getLogger(__name__)


class MediaPipeFaceDetector(IFaceDetector):
    """Face detector implementation using MediaPipe."""

    def __init__(self, min_detection_confidence: float = 0.5):
        """
        Initialize MediaPipe face detector.

        Args:
            min_detection_confidence: Minimum confidence threshold for detection (0.0-1.0)
        """
        self._min_detection_confidence = min_detection_confidence
        self._mp_face_detection = mp.solutions.face_detection
        logger.info(
            f"MediaPipe face detector initialized with confidence threshold: "
            f"{min_detection_confidence}"
        )

    def detect_face(self, image_data: bytes) -> FaceDetectionResult:
        """
        Detect faces in the provided image using MediaPipe.

        Args:
            image_data: Raw image bytes

        Returns:
            FaceDetectionResult with detection status

        Raises:
            ValueError: If image data is invalid or cannot be processed
        """
        try:
            # Convert bytes to numpy array
            image_array = self._bytes_to_image(image_data)

            # Perform face detection
            with self._mp_face_detection.FaceDetection(
                min_detection_confidence=self._min_detection_confidence
            ) as face_detection:
                # Convert BGR to RGB (MediaPipe uses RGB)
                rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

                # Process the image
                results = face_detection.process(rgb_image)

                # Check if any faces were detected
                face_detected = (
                    results.detections is not None and len(results.detections) > 0
                )

                if face_detected:
                    logger.debug(f"Detected {len(results.detections)} face(s)")
                    # Get the highest confidence score
                    confidence = max(
                        detection.score[0] for detection in results.detections
                    )
                else:
                    logger.debug("No faces detected")
                    confidence = None

                return FaceDetectionResult(
                    face_detected=face_detected, confidence=confidence
                )

        except Exception as e:
            logger.error(f"Error during face detection: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")

    def _bytes_to_image(self, image_data: bytes) -> np.ndarray:
        """
        Convert image bytes to numpy array.

        Args:
            image_data: Raw image bytes

        Returns:
            Numpy array representing the image

        Raises:
            ValueError: If image cannot be decoded
        """
        try:
            # Try to open with PIL first
            pil_image = Image.open(BytesIO(image_data))
            # Convert to RGB if necessary
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")  # type: ignore[assignment]
            # Convert PIL Image to numpy array
            image_array = np.array(pil_image)
            # Convert RGB to BGR for OpenCV
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            return image_array
        except Exception as e:
            logger.error(f"Failed to decode image: {str(e)}")
            raise ValueError(f"Invalid image data: {str(e)}")
