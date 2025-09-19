import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import os

from main import app

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'AIRTABLE_TOKEN': 'test_token',
        'BASE_ID': 'test_base_id',
        'MAPBOX_TOKEN': 'test_mapbox_token',
        'GOOGLE_MAPS_API_KEY': 'test_google_key',
        'GEMINI_API_KEY': 'test_gemini_key',
        'SMTP_HOST': 'smtp.test.com',
        'SMTP_PORT': '587',
        'SMTP_USER': 'test@test.com',
        'SMTP_PASS': 'test_password'
    }):
        yield

@pytest.fixture
def sample_warehouse_data():
    """Sample warehouse data for testing"""
    return {
        "id": "rec123",
        "fields": {
            "City": "Test City",
            "State": "CA",
            "Zip": 90210,
            "Name": "Test Warehouse",
            "Status": "Active",
            "Tier": "Gold",
            "Contact_1": "John Doe",
            "Email_1": "john@test.com",
            "createdTime": "2023-01-01T00:00:00.000Z"
        }
    }

@pytest.fixture
def sample_location_request():
    """Sample location request for testing"""
    return {
        "zip_code": "90210",
        "radius_miles": 50.0
    }

@pytest.fixture
def sample_email_data():
    """Sample email data for testing"""
    return {
        "email_subject": "Test Subject",
        "email_body": "Test body",
        "emails_data": [
            {
                "email": "test@example.com",
                "services": ["storage", "shipping"],
                "adress": "123 Test St"
            }
        ]
    }
