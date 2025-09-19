import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import requests
import httpx

from services.geolocation.geolocation_service import (
    haversine,
    get_coordinates_mapbox,
    get_coordinates_google,
    get_driving_distance_and_time_mapbox,
    get_driving_distance_and_time_google
)

class TestGeolocationService:
    """Test cases for geolocation service functions"""

    def test_haversine(self):
        """Test haversine distance calculation"""
        # Test distance between LA and NYC (approximately 2440 miles)
        la_coords = (34.0522, -118.2437)
        nyc_coords = (40.7128, -74.0060)
        
        distance = haversine(la_coords[0], la_coords[1], nyc_coords[0], nyc_coords[1])
        
        # Should be approximately 2440 miles (allowing for some variance)
        assert 2400 < distance < 2500
        
        # Test same coordinates (should be 0)
        distance = haversine(la_coords[0], la_coords[1], la_coords[0], la_coords[1])
        assert distance == 0

    @patch('requests.get')
    def test_get_coordinates_mapbox_success(self, mock_get, mock_env_vars):
        """Test successful coordinate fetching from Mapbox"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "features": [
                {
                    "center": [-118.2437, 34.0522]  # [lon, lat]
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = get_coordinates_mapbox("90210")
        
        assert result == (34.0522, -118.2437)  # (lat, lon)

    @patch('requests.get')
    def test_get_coordinates_mapbox_no_features(self, mock_get, mock_env_vars):
        """Test Mapbox coordinate fetching with no features"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = get_coordinates_mapbox("invalid")
        
        assert result is None

    @patch('requests.get')
    def test_get_coordinates_mapbox_error(self, mock_get, mock_env_vars):
        """Test Mapbox coordinate fetching with error"""
        mock_get.side_effect = requests.RequestException("Test error")
        
        result = get_coordinates_mapbox("90210")
        
        assert result is None

    @patch('services.geolocation.geolocation_service.gmaps')
    def test_get_coordinates_google_success(self, mock_gmaps, mock_env_vars):
        """Test successful coordinate fetching from Google"""
        mock_gmaps.geocode.return_value = [
            {
                'geometry': {
                    'location': {'lat': 34.0522, 'lng': -118.2437}
                }
            }
        ]
        
        result = get_coordinates_google("90210")
        
        assert result == (34.0522, -118.2437)

    @patch('services.geolocation.geolocation_service.gmaps')
    def test_get_coordinates_google_no_results(self, mock_gmaps, mock_env_vars):
        """Test Google coordinate fetching with no results"""
        mock_gmaps.geocode.return_value = []
        
        result = get_coordinates_google("invalid")
        
        assert result is None

    @patch('services.geolocation.geolocation_service.gmaps')
    def test_get_coordinates_google_error(self, mock_gmaps, mock_env_vars):
        """Test Google coordinate fetching with error"""
        mock_gmaps.geocode.side_effect = Exception("Test error")
        
        result = get_coordinates_google("90210")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_driving_distance_and_time_mapbox_success(self, mock_env_vars):
        """Test successful driving distance/time from Mapbox"""
        mock_response = {
            "routes": [
                {
                    "distance": 16093.4,  # 10 miles in meters
                    "duration": 1800  # 30 minutes in seconds
                }
            ]
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            
            # Create a mock response object
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            
            mock_instance.get = AsyncMock(return_value=mock_response_obj)
            
            result = await get_driving_distance_and_time_mapbox(
                (34.0522, -118.2437), (34.0622, -118.2537)
            )
            
            assert result["distance_miles"] == pytest.approx(10.0, rel=0.1)
            assert result["duration_minutes"] == 30.0

    @pytest.mark.asyncio
    async def test_get_driving_distance_and_time_mapbox_no_routes(self, mock_env_vars):
        """Test Mapbox driving distance/time with no routes"""
        mock_response = {"routes": []}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            
            # Create a mock response object
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            
            mock_instance.get = AsyncMock(return_value=mock_response_obj)
            
            result = await get_driving_distance_and_time_mapbox(
                (34.0522, -118.2437), (34.0622, -118.2537)
            )
            
            assert result is None

    @patch('services.geolocation.geolocation_service.gmaps')
    def test_get_driving_distance_and_time_google_success(self, mock_gmaps, mock_env_vars):
        """Test successful driving distance/time from Google"""
        mock_gmaps.directions.return_value = [
            {
                'legs': [
                    {
                        'distance': {'value': 16093.4},  # 10 miles in meters
                        'duration': {'value': 1800}  # 30 minutes in seconds
                    }
                ]
            }
        ]
        
        result = get_driving_distance_and_time_google(
            (34.0522, -118.2437), (34.0622, -118.2537)
        )
        
        # The function is async, so we need to await it
        import asyncio
        result = asyncio.run(result)
        
        assert result["distance_miles"] == pytest.approx(10.0, rel=0.1)
        assert result["duration_minutes"] == 30.0

    @patch('services.geolocation.geolocation_service.gmaps')
    def test_get_driving_distance_and_time_google_no_results(self, mock_gmaps, mock_env_vars):
        """Test Google driving distance/time with no results"""
        mock_gmaps.directions.return_value = []
        
        result = get_driving_distance_and_time_google(
            (34.0522, -118.2437), (34.0622, -118.2537)
        )
        
        # The function is async, so we need to await it
        import asyncio
        result = asyncio.run(result)
        
        assert result is None
