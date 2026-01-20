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
git clone https://github.com/DamithT2001/ai-face-detection-service.git
cd ai-face-detection-service
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
- **Endpoint**: `POST /api/v1/detect-face`
- **Description**: Upload an image to detect if it contains a human face
- **Request**: Multipart form data with an image file
- **Response**: JSON with `face_detected` boolean

#### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check service health and version
- **Response**: JSON with status and version

### Example Usage

#### Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/detect-face" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/image.jpg"
```

#### Using Python
```python
import requests

url = "http://localhost:8000/api/v1/detect-face"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())  # {"face_detected": true}
```

#### Using JavaScript/Node.js
```javascript
const fs = require('fs');
const FormData = require('form-data');
const fetch = require('node-fetch');

const form = new FormData();
form.append('file', fs.createReadStream('image.jpg'));

fetch('http://localhost:8000/api/v1/detect-face', {
  method: 'POST',
  body: form
})
.then(res => res.json())
.then(data => console.log(data));  // {face_detected: true}
```

### API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Configuration

Configuration can be managed through environment variables. Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
```

Available configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
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

### Project Structure

```
ai-face-detection-service/
├── app/
│   ├── domain/              # Domain layer
│   │   ├── models.py        # Domain models
│   │   └── interfaces.py    # Domain interfaces
│   ├── application/         # Application layer
│   │   └── face_detection_service.py  # Use cases
│   ├── infrastructure/      # Infrastructure layer
│   │   └── mediapipe_detector.py  # MediaPipe implementation
│   ├── api/                 # API layer
│   │   ├── endpoints.py     # API routes
│   │   ├── schemas.py       # Request/response models
│   │   ├── dependencies.py  # Dependency injection
│   │   └── config.py        # Configuration
│   └── main.py              # Application entry point
├── tests/                   # Test suite
│   ├── test_domain.py
│   ├── test_application.py
│   ├── test_infrastructure.py
│   └── test_api.py
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # This file
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

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.