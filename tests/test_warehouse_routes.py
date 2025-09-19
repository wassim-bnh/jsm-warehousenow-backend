import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

class TestWarehouseRoutes:
    """Test cases for warehouse API endpoints"""

    @pytest.mark.asyncio
    async def test_warehouses_endpoint_success(self, client, mock_env_vars, sample_warehouse_data):
        """Test successful warehouses endpoint"""
        with patch('warehouse.warehouse_route.fetch_warehouses_from_airtable', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = [sample_warehouse_data]
            
            response = client.get("/warehouses")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["data"]) == 1
            assert data["data"][0]["id"] == "rec123"

    @pytest.mark.asyncio
    async def test_warehouses_endpoint_error(self, client, mock_env_vars):
        """Test warehouses endpoint with error"""
        with patch('warehouse.warehouse_route.fetch_warehouses_from_airtable', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.side_effect = Exception("Test error")
            
            response = client.get("/warehouses")
            
            assert response.status_code == 500
            data = response.json()
            assert "Unexpected error" in data["detail"]

    @pytest.mark.asyncio
    async def test_nearby_warehouses_endpoint_success(self, client, mock_env_vars, sample_location_request, sample_warehouse_data):
        """Test successful nearby warehouses endpoint"""
        mock_result = {
            "origin_zip": "90210",
            "warehouses": [sample_warehouse_data],
            "ai_analysis": "Test analysis"
        }
        
        with patch('warehouse.warehouse_service.find_nearby_warehouses', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = mock_result
            
            response = client.post("/nearby_warehouses", json=sample_location_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["data"]["origin_zip"] == "90210"

    @pytest.mark.asyncio
    async def test_nearby_warehouses_endpoint_invalid_request(self, client, mock_env_vars):
        """Test nearby warehouses endpoint with invalid request"""
        invalid_request = {}  # Missing required zip_code field
        
        response = client.post("/nearby_warehouses", json=invalid_request)
        
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_send_email_endpoint_success(self, client, mock_env_vars, sample_email_data):
        """Test successful send email endpoint"""
        mock_result = [{"status": "success", "to": "test@example.com"}]
        
        with patch('services.messaging.email_service.send_bulk_email', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = mock_result
            
            response = client.post("/send_email", json=sample_email_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["data"]) == 1

    @pytest.mark.asyncio
    async def test_send_email_endpoint_error(self, client, mock_env_vars, sample_email_data):
        """Test send email endpoint with error"""
        with patch('warehouse.warehouse_route.send_bulk_email', new_callable=AsyncMock) as mock_send:
            mock_send.side_effect = Exception("Email error")
            
            response = client.post("/send_email", json=sample_email_data)
            
            assert response.status_code == 500
            data = response.json()
            assert "Unexpected error" in data["detail"]
