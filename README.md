# JSM WarehouseNow Backend API

A FastAPI-based backend service for warehouse management and geolocation services.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Environment variables configured

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jsm-warehousenow-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with the following variables:
   ```env
   MAPBOX_TOKEN=your_mapbox_token
   AIRTABLE_TOKEN=your_airtable_token
   BASE_ID=your_airtable_base_id
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`

## 🏢 Warehouse Endpoints

### Get All Warehouses
```http
GET /warehouses
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "rec123",
      "fields": {
        "City": "New York",
        "State": "NY",
        "Zip": 10001,
        "Name": "Warehouse A",
        "Status": "Active",
        "Tier": "Premium",
        "Contact_1": "John Doe",
        "Email_1": "john@warehouse.com",
        "Office_number": "+1-555-0123",
        "Cell_number_1": "+1-555-0124",
        "Hours": "24/7",
        "Hazmat": "Yes",
        "Temp_Control": "Yes",
        "Food_Grade": "No",
        "Services": ["Storage", "Shipping"],
        "Website": "https://warehouse.com",
        "createdTime": "2024-01-01T00:00:00.000Z"
      }
    }
  ]
}
```

### Find Nearby Warehouses
```http
POST /nearby_warehouses
```

**Request Body:**
```json
{
  "zip_code": "10001",
  "radius_miles": 50
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "origin_zip": "10001",
    "warehouses": [
      {
        "id": "rec123",
        "fields": { /* warehouse fields */ },
        "distance_miles": 15.2,
        "duration_minutes": 25.5
      }
    ]
  }
}
```

## 🗺️ Geolocation Services

### Services Overview

The geolocation module provides:

1. **Coordinate Lookup**: Convert ZIP codes to latitude/longitude coordinates
2. **Distance Calculation**: Calculate driving distance and time between locations
3. **Haversine Distance**: Calculate straight-line distance between coordinates

### Key Functions

- `get_coordinates(zip_code)`: Convert ZIP code to coordinates using Mapbox Geocoding API
- `get_driving_distance_and_time_mapbox(origin, destination)`: Get driving distance and time using Mapbox Directions API
- `haversine(lat1, lon1, lat2, lon2)`: Calculate straight-line distance between two points

## 🏗️ Project Structure

```
jsm-warehousenow-backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── geolocation/
│   ├── route.py           # Geolocation API routes
│   └── geolocation_service.py  # Geolocation business logic
└── warehouse/
    ├── models.py          # Pydantic data models
    ├── warehouse_route.py # Warehouse API routes
    └── warehouse_service.py    # Warehouse business logic
```

## 🧪 Testing

### Running Tests

The project includes comprehensive unit tests using pytest. To run the tests:

1. **Install test dependencies** (included in requirements.txt)
   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests**
   ```bash
   python run_tests.py
   ```
   
   Or directly with pytest:
   ```bash
   pytest tests/ -v
   ```

3. **Run specific test files**
   ```bash
   python run_tests.py tests/test_warehouse_routes.py
   pytest tests/test_warehouse_routes.py -v
   ```

4. **Run tests with coverage**
   ```bash
   pytest tests/ --cov=warehouse --cov=services --cov-report=html
   ```

### Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── test_warehouse_routes.py       # API endpoint tests
├── test_warehouse_service.py      # Warehouse service tests
├── test_geolocation_service.py    # Geolocation service tests
├── test_email_service.py          # Email service tests
├── test_ai_analysis.py            # AI analysis tests
└── test_models.py                 # Pydantic model tests
```

### Test Coverage

The test suite covers:
- ✅ API endpoints (success and error cases)
- ✅ Service layer functions
- ✅ Data models validation
- ✅ External API integrations (mocked)
- ✅ Error handling scenarios

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MAPBOX_TOKEN` | Mapbox API token for geocoding and directions | Yes |
| `AIRTABLE_TOKEN` | Airtable API token for warehouse data | Yes |
| `BASE_ID` | Airtable base ID containing warehouse data | Yes |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key for geocoding and directions | Yes |
| `GEMINI_API_KEY` | Google Gemini API key for AI analysis | Yes |
| `SMTP_HOST` | SMTP server host for email sending | Yes |
| `SMTP_PORT` | SMTP server port | Yes |
| `SMTP_USER` | SMTP username | Yes |
| `SMTP_PASS` | SMTP password | Yes |

### External Services

- **Mapbox**: Geocoding and directions API
- **Airtable**: Warehouse data storage and retrieval
- **Google Maps**: Alternative geocoding and directions API
- **Google Gemini**: AI analysis for warehouse recommendations
- **SMTP Server**: Email delivery service