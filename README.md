# Human Face Detection REST API

A production-ready REST API for detecting human faces in images using MediaPipe and FastAPI.

## Features

- **Simple REST API**: Upload an image and receive a boolean indicating whether a human face was detected
- **MediaPipe Integration**: Uses Google's MediaPipe pre-trained face detection model
- **Clean Architecture**: Modular, testable, and maintainable code structure
- **Production Ready**: Comprehensive error handling, logging, and configuration management
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Well Tested**: Comprehensive unit and integration tests
- **API Documentation**: Auto-generated interactive API docs with Swagger UI and ReDoc

## API Response

```json
{
  "face_detected": true
}
```

## Architecture

The service follows clean architecture principles with clear separation of concerns:

```
app/
├── domain/          # Domain models and interfaces
├── application/     # Business logic and use cases
├── infrastructure/  # External implementations (MediaPipe)
└── api/            # FastAPI endpoints and schemas
```

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/DamithT2001/face-detection-service-py.git
cd face-detection-service-py
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### Using Docker

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. Or build and run with Docker:
```bash
docker build -t face-detection-api .
docker run -p 8000:8000 face-detection-api
```

## Usage

### API Endpoints

#### Detect Face
- **Endpoint**: `POST /api/detect-face`
- **Description**: Upload an image to detect if it contains a human face
- **Request**: Multipart form data with an image file
- **Response**: JSON with `face_detected` boolean

#### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check service health and version
- **Response**: JSON with status and version

### API Documentation

Once the service is running, access the API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Configuration

Configuration can be managed through environment variables. Copy `.env.example` to `.env` and adjust values:

Available configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `localhost` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `false` |
| `MIN_DETECTION_CONFIDENCE` | Face detection confidence threshold (0.0-1.0) | `0.5` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

### Running Tests

Run all tests with coverage:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_api.py
```

Run with verbose output:
```bash
pytest -v
```

### Code Quality

Format code with Black:
```bash
black app/ tests/
```

Lint with flake8:
```bash
flake8 app/ tests/
```

Type check with mypy:
```bash
mypy app/
```

## Design Decisions

### Clean Architecture
The service follows clean architecture principles with clear separation between:
- **Domain Layer**: Core business entities and interfaces
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: External implementations (MediaPipe)
- **API Layer**: HTTP interface (FastAPI)

This ensures the code is:
- **Testable**: Each layer can be tested independently
- **Maintainable**: Changes in one layer don't affect others
- **Flexible**: Easy to swap implementations

### MediaPipe Face Detection
- Uses MediaPipe's pre-trained face detection model (short-range model)
- No custom ML models or training required
- Lightweight and fast inference
- Configurable confidence threshold

### Response Format
The API returns only `{"face_detected": boolean}` as specified, keeping the response simple and focused on the core requirement.

## Performance

- Average response time: ~100-300ms per image (depends on image size)
- Supports common image formats: JPEG, PNG, BMP, etc.
- Recommended image size: Up to 2MB for optimal performance

## Security Considerations

- Non-root user in Docker container
- Input validation on file uploads
- No data persistence (images are not stored)
- CORS configured (adjust for production)
- Comprehensive error handling
