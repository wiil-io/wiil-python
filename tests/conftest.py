"""Pytest configuration and shared fixtures for WIIL SDK tests."""

import pytest
import responses

from wiil import WiilClient


# Test configuration
BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


@pytest.fixture
def client() -> WiilClient:
    """Create a test WiilClient instance."""
    return WiilClient(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture
def mock_api():
    """Enable responses HTTP mocking for tests."""
    with responses.RequestsMock() as rsps:
        yield rsps


def create_api_response(data: any, success: bool = True) -> dict:
    """Create a standardized API response."""
    import time
    return {
        "success": success,
        "data": data,
        "metadata": {
            "timestamp": int(time.time() * 1000),
            "version": "v1"
        }
    }


def create_error_response(code: str, message: str) -> dict:
    """Create a standardized error response (flat structure)."""
    import time
    return {
        "success": False,
        "code": code,
        "message": message,
        "meta": {
            "timestamp": int(time.time() * 1000),
            "version": "v1"
        }
    }


@pytest.fixture
def api_response():
    """Fixture for creating API responses."""
    return create_api_response


@pytest.fixture
def error_response():
    """Fixture for creating error responses."""
    return create_error_response
