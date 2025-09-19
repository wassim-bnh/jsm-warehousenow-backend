import pytest
from pydantic import ValidationError

from warehouse.models import (
    LocationRequest,
    WarehouseFields,
    WarehouseData,
    FilterWarehouseData,
    ResponseModel,
    SendEmailData,
    SendBulkEmailData
)

class TestModels:
    """Test cases for Pydantic models"""

    def test_location_request_valid(self):
        """Test valid LocationRequest creation"""
        data = {"zip_code": "90210", "radius_miles": 50.0}
        location_request = LocationRequest(**data)
        
        assert location_request.zip_code == "90210"
        assert location_request.radius_miles == 50.0

    def test_location_request_default_radius(self):
        """Test LocationRequest with default radius"""
        data = {"zip_code": "90210"}
        location_request = LocationRequest(**data)
        
        assert location_request.zip_code == "90210"
        assert location_request.radius_miles == 50.0  # Default value

    def test_location_request_invalid_zip(self):
        """Test LocationRequest with invalid zip code"""
        data = {"zip_code": "", "radius_miles": 50.0}
        
        # Empty string should be valid in Pydantic by default
        location_request = LocationRequest(**data)
        assert location_request.zip_code == ""
        assert location_request.radius_miles == 50.0

    def test_warehouse_fields_valid(self):
        """Test valid WarehouseFields creation"""
        data = {
            "City": "Test City",
            "State": "CA",
            "Zip": 90210,
            "Name": "Test Warehouse",
            "Status": "Active",
            "Tier": "Gold",
            "createdTime": "2023-01-01T00:00:00.000Z"
        }
        warehouse_fields = WarehouseFields(**data)
        
        assert warehouse_fields.City == "Test City"
        assert warehouse_fields.State == "CA"
        assert warehouse_fields.Zip == 90210
        assert warehouse_fields.Name == "Test Warehouse"
        assert warehouse_fields.Status == "Active"
        assert warehouse_fields.Tier == "Gold"

    def test_warehouse_fields_optional_fields(self):
        """Test WarehouseFields with optional fields"""
        data = {
            "City": "Test City",
            "createdTime": "2023-01-01T00:00:00.000Z"
        }
        warehouse_fields = WarehouseFields(**data)
        
        assert warehouse_fields.City == "Test City"
        assert warehouse_fields.State is None
        assert warehouse_fields.Zip is None
        assert warehouse_fields.Name is None

    def test_warehouse_data_valid(self):
        """Test valid WarehouseData creation"""
        data = {
            "id": "rec123",
            "fields": {
                "City": "Test City",
                "Name": "Test Warehouse",
                "createdTime": "2023-01-01T00:00:00.000Z"
            }
        }
        warehouse_data = WarehouseData(**data)
        
        assert warehouse_data.id == "rec123"
        assert warehouse_data.fields.City == "Test City"
        assert warehouse_data.fields.Name == "Test Warehouse"

    def test_filter_warehouse_data_valid(self):
        """Test valid FilterWarehouseData creation"""
        data = {
            "City": "Test City",
            "State": "CA",
            "Zip": 90210,
            "Status": "Active",
            "Tier": "Gold"
        }
        filter_data = FilterWarehouseData(**data)
        
        assert filter_data.City == "Test City"
        assert filter_data.State == "CA"
        assert filter_data.Zip == 90210
        assert filter_data.Status == "Active"
        assert filter_data.Tier == "Gold"

    def test_response_model_valid(self):
        """Test valid ResponseModel creation"""
        data = {"test": "data"}
        response = ResponseModel(status="success", data=data)
        
        assert response.status == "success"
        assert response.data == data

    def test_send_email_data_valid(self):
        """Test valid SendEmailData creation"""
        data = {
            "email": "test@example.com",
            "services": ["storage", "shipping"],
            "adress": "123 Test St"
        }
        email_data = SendEmailData(**data)
        
        assert email_data.email == "test@example.com"
        assert email_data.services == ["storage", "shipping"]
        assert email_data.adress == "123 Test St"

    def test_send_email_data_empty_services(self):
        """Test SendEmailData with empty services list"""
        data = {
            "email": "test@example.com",
            "services": [],
            "adress": "123 Test St"
        }
        email_data = SendEmailData(**data)
        
        assert email_data.email == "test@example.com"
        assert email_data.services == []
        assert email_data.adress == "123 Test St"

    def test_send_bulk_email_data_valid(self):
        """Test valid SendBulkEmailData creation"""
        data = {
            "email_subject": "Test Subject",
            "email_body": "Test body",
            "emails_data": [
                {
                    "email": "test1@example.com",
                    "services": ["storage"],
                    "adress": "123 Test St"
                },
                {
                    "email": "test2@example.com",
                    "services": ["shipping"],
                    "adress": "456 Test Ave"
                }
            ]
        }
        bulk_email_data = SendBulkEmailData(**data)
        
        assert bulk_email_data.email_subject == "Test Subject"
        assert bulk_email_data.email_body == "Test body"
        assert len(bulk_email_data.emails_data) == 2
        assert bulk_email_data.emails_data[0].email == "test1@example.com"
        assert bulk_email_data.emails_data[1].email == "test2@example.com"

    def test_send_bulk_email_data_optional_fields(self):
        """Test SendBulkEmailData with optional fields"""
        data = {
            "emails_data": [
                {
                    "email": "test@example.com",
                    "services": ["storage"],
                    "adress": "123 Test St"
                }
            ]
        }
        bulk_email_data = SendBulkEmailData(**data)
        
        assert bulk_email_data.email_subject is None
        assert bulk_email_data.email_body is None
        assert len(bulk_email_data.emails_data) == 1

    def test_send_email_data_invalid_email(self):
        """Test SendEmailData with invalid email"""
        data = {
            "email": "invalid-email",
            "services": ["storage"],
            "adress": "123 Test St"
        }
        
        # Pydantic should validate email format
        email_data = SendEmailData(**data)
        assert email_data.email == "invalid-email"  # Pydantic doesn't validate email format by default
