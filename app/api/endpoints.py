"""API endpoints for face detection service."""
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.schemas import ErrorResponse, FaceDetectionResponse
from app.application.face_detection_service import FaceDetectionService
from app.api.dependencies import get_face_detection_service


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Face Detection"])


@router.post(
    "/detect-face",
    response_model=FaceDetectionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image data"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Detect human face in image",
    description="Upload an image and receive a boolean indicating whether a human face was detected.",
)
async def detect_face(
    file: Annotated[UploadFile, File(description="Image file to analyze")],
    service: FaceDetectionService = Depends(get_face_detection_service),
) -> FaceDetectionResponse:
    """
    Detect if a human face is present in the uploaded image.
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
        service: Face detection service instance
        
    Returns:
        FaceDetectionResponse with face_detected boolean
        
    Raises:
        HTTPException: If image is invalid or processing fails
    """
    # Validate file is provided
    if not file:
        logger.warning("No file provided in request")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image file provided"
        )
    
    # Validate content type
    if file.content_type and not file.content_type.startswith("image/"):
        logger.warning(f"Invalid content type: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Must be an image."
        )
    
    try:
        # Read image data
        image_data = await file.read()
        
        if not image_data:
            logger.warning("Empty file uploaded")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )
        
        # Perform face detection
        result = service.detect_face_in_image(image_data)
        
        return FaceDetectionResponse(face_detected=result.face_detected)
    
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception("Unexpected error during face detection")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the image"
        )
