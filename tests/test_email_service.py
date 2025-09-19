import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import aiosmtplib

from services.messaging.email_service import send_bulk_email, send_email
from warehouse.models import SendBulkEmailData, SendEmailData

class TestEmailService:
    """Test cases for email service functions"""

    @pytest.mark.asyncio
    async def test_send_bulk_email_success(self, mock_env_vars):
        """Test successful bulk email sending"""
        email_data = SendBulkEmailData(
            email_subject="Test Subject",
            email_body="Test body",
            emails_data=[
                SendEmailData(
                    email="test1@example.com",
                    services=["storage"],
                    adress="123 Test St"
                ),
                SendEmailData(
                    email="test2@example.com",
                    services=["shipping", "storage"],
                    adress="456 Test Ave"
                )
            ]
        )
        
        with patch('services.messaging.email_service.send_email', new_callable=AsyncMock) as mock_send:
            mock_send.side_effect = [
                {"status": "success", "to": "test1@example.com"},
                {"status": "success", "to": "test2@example.com"}
            ]
            
            result = await send_bulk_email(email_data)
            
            assert len(result) == 2
            assert result[0]["status"] == "success"
            assert result[1]["status"] == "success"
            assert mock_send.call_count == 2

    @pytest.mark.asyncio
    async def test_send_email_success(self, mock_env_vars):
        """Test successful single email sending"""
        email_data = SendEmailData(
            email="test@example.com",
            services=["storage", "shipping"],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.return_value = None
            
            result = await send_email("Test Subject", "Test body", email_data)
            
            assert result["status"] == "success"
            assert result["to"] == "test@example.com"
            mock_smtp.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_email_with_default_subject(self, mock_env_vars):
        """Test email sending with default subject generation"""
        email_data = SendEmailData(
            email="test@example.com",
            services=["storage", "shipping"],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.return_value = None
            
            result = await send_email(None, "Test body", email_data)
            
            assert result["status"] == "success"
            # Should generate subject with services
            mock_smtp.assert_called_once()
            call_args = mock_smtp.call_args[0][0]
            assert "storage and shipping" in call_args["Subject"]

    @pytest.mark.asyncio
    async def test_send_email_with_single_service(self, mock_env_vars):
        """Test email sending with single service"""
        email_data = SendEmailData(
            email="test@example.com",
            services=["storage"],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.return_value = None
            
            result = await send_email(None, "Test body", email_data)
            
            assert result["status"] == "success"
            mock_smtp.assert_called_once()
            call_args = mock_smtp.call_args[0][0]
            assert "storage" in call_args["Subject"]

    @pytest.mark.asyncio
    async def test_send_email_with_no_services(self, mock_env_vars):
        """Test email sending with no services specified"""
        email_data = SendEmailData(
            email="test@example.com",
            services=[],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.return_value = None
            
            result = await send_email(None, "Test body", email_data)
            
            assert result["status"] == "success"
            mock_smtp.assert_called_once()
            call_args = mock_smtp.call_args[0][0]
            assert "general warehousing services" in call_args["Subject"]

    @pytest.mark.asyncio
    async def test_send_email_with_default_body(self, mock_env_vars):
        """Test email sending with default HTML body"""
        email_data = SendEmailData(
            email="test@example.com",
            services=["storage"],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.return_value = None
            
            result = await send_email("Test Subject", None, email_data)
            
            assert result["status"] == "success"
            mock_smtp.assert_called_once()
            call_args = mock_smtp.call_args[0][0]
            # Should contain default HTML body
            assert "WarehouseNow Team" in str(call_args.get_payload()[1].get_payload())

    @pytest.mark.asyncio
    async def test_send_email_smtp_error(self, mock_env_vars):
        """Test email sending with SMTP error"""
        email_data = SendEmailData(
            email="test@example.com",
            services=["storage"],
            adress="123 Test St"
        )
        
        with patch('aiosmtplib.send', new_callable=AsyncMock) as mock_smtp:
            mock_smtp.side_effect = Exception("SMTP error")
            
            result = await send_email("Test Subject", "Test body", email_data)
            
            assert result["status"] == "error"
            assert result["to"] == "test@example.com"
            assert "SMTP error" in result["error"]
