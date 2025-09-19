import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from services.gemini_services.ai_analysis import (
    analyze_warehouse_with_gemini,
    GENERAL_AI_ANALYSIS
)

class TestAIAnalysis:
    """Test cases for AI analysis service"""

    def test_general_ai_analysis_constant(self):
        """Test that GENERAL_AI_ANALYSIS constant is defined"""
        assert GENERAL_AI_ANALYSIS is not None
        assert isinstance(GENERAL_AI_ANALYSIS, str)
        assert len(GENERAL_AI_ANALYSIS) > 0

    @pytest.mark.asyncio
    async def test_analyze_warehouse_with_gemini_success(self, mock_env_vars):
        """Test successful AI analysis with Gemini"""
        sample_warehouses = [
            {
                "fields": {"Name": "Warehouse A", "Tier": "Gold"},
                "distance_miles": 10.5,
                "duration_minutes": 15.0,
                "has_missed_fields": False
            },
            {
                "fields": {"Name": "Warehouse B", "Tier": "Silver"},
                "distance_miles": 20.0,
                "duration_minutes": 25.0,
                "has_missed_fields": True
            },
            {
                "fields": {"Name": "Warehouse C", "Tier": "Bronze"},
                "distance_miles": 30.0,
                "duration_minutes": 35.0,
                "has_missed_fields": False
            }
        ]
        
        mock_response = MagicMock()
        mock_response.text = "Test AI analysis response"
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_model.generate_content_async = AsyncMock(return_value=mock_response)
            
            result = await analyze_warehouse_with_gemini(sample_warehouses)
            
            assert result == "Test AI analysis response"
            mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_warehouse_with_gemini_empty_list(self, mock_env_vars):
        """Test AI analysis with empty warehouse list"""
        mock_response = MagicMock()
        mock_response.text = "No warehouses found"
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_model.generate_content_async = AsyncMock(return_value=mock_response)
            
            result = await analyze_warehouse_with_gemini([])
            
            assert result == "No warehouses found"
            mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_warehouse_with_gemini_single_warehouse(self, mock_env_vars):
        """Test AI analysis with single warehouse"""
        sample_warehouses = [
            {
                "fields": {"Name": "Warehouse A", "Tier": "Gold"},
                "distance_miles": 10.5,
                "duration_minutes": 15.0,
                "has_missed_fields": False
            }
        ]
        
        mock_response = MagicMock()
        mock_response.text = "Single warehouse analysis"
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_model.generate_content_async = AsyncMock(return_value=mock_response)
            
            result = await analyze_warehouse_with_gemini(sample_warehouses)
            
            assert result == "Single warehouse analysis"
            mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_warehouse_with_gemini_missing_fields(self, mock_env_vars):
        """Test AI analysis with warehouses having missing fields"""
        sample_warehouses = [
            {
                "fields": {"Name": "Warehouse A", "Tier": "Gold"},
                "distance_miles": 10.5,
                "duration_minutes": 15.0,
                "has_missed_fields": True
            },
            {
                "fields": {"Name": "Warehouse B", "Tier": "Silver"},
                "distance_miles": 20.0,
                "duration_minutes": 25.0,
                "has_missed_fields": True
            }
        ]
        
        mock_response = MagicMock()
        mock_response.text = "Analysis with missing fields"
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_model.generate_content_async = AsyncMock(return_value=mock_response)
            
            result = await analyze_warehouse_with_gemini(sample_warehouses)
            
            assert result == "Analysis with missing fields"
            mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_warehouse_with_gemini_error_handling(self, mock_env_vars):
        """Test AI analysis error handling"""
        sample_warehouses = [
            {
                "fields": {"Name": "Warehouse A", "Tier": "Gold"},
                "distance_miles": 10.5,
                "duration_minutes": 15.0,
                "has_missed_fields": False
            }
        ]
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_model.generate_content_async.side_effect = Exception("API Error")
            
            # This should raise an exception, which would be handled by the calling function
            with pytest.raises(Exception):
                await analyze_warehouse_with_gemini(sample_warehouses)
