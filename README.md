# Data API Service

This service provides endpoints to manage and retrieve sample data.

## API Documentation

The API documentation is available through Swagger UI when the service is running. You can access it at:

```
http://localhost:5000
```

## API Endpoints

### Get Sample Data
- **URL**: `/v1/api/data/sample`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "sample_id": "integer"
  }
  ```
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "content": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - 400 Bad Request (Missing sample_id)
  - 404 Not Found (Invalid sample_id)
  - 500 Internal Server Error

## Postman Collection

A Postman collection is available in the `postman-collections` directory for testing the API endpoints. The collection includes:
- Success case
- Bad request case (missing sample_id)
- Not found case (invalid sample_id)

### Using the Postman Collection

1. Import the collection from `postman-collections/data.json`
2. Create an environment in Postman
3. Set the environment variable:
   - `base_url`: `http://localhost:5000`
4. Run the collection

## Setup and Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application (from the project root directory):
   ```bash
   # Method 1 (preferred)
   python -m app.main

   # Method 2 (alternative)
   PYTHONPATH=$PYTHONPATH:. python app/main.py
   ```

The server will start at `http://localhost:5000`. By default, it runs in development mode with logging level set to INFO. The environment and logging level can be configured through the application's configuration.

## Environment Configuration

The application supports different environments through the `Config.ENV` setting:
- Development (default): Full logging and Swagger UI enabled
- Production: Swagger UI disabled, configurable logging level

You can set the logging level through the `LOG_LEVEL` configuration (defaults to "INFO").

## Development

The project follows a standard Flask application structure:
- `app/`: Main application directory
  - `api/`: API endpoints
  - `controllers/`: Business logic
  - `models/`: Database models
  - `repositories/`: Data access layer
  - `utils/`: Utility functions and constants
  - `main.py`: Application entry point
