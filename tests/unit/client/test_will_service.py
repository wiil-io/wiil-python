"""Tests for WillService client."""

import pytest

from wiil.client.will_service import WillService
from wiil.errors import WiilConfigurationError


class _DummyResponse:
    pass


def test_will_service_defaults_to_ott_base_url():
    """WillService should default to OTT base URL."""
    service = WillService(api_key="test-key")

    assert service.config.base_url == "https://ott.wiil.io"
    assert service.config.timeout == 30


def test_will_service_exposes_service_helpers():
    """WillService should expose ott and translation helpers."""
    service = WillService(api_key="test-key")

    assert hasattr(service, "ott")
    assert hasattr(service, "translation")


def test_will_service_validates_api_key():
    """WillService should reject missing/blank API keys."""
    with pytest.raises(WiilConfigurationError):
        WillService(api_key="")

    with pytest.raises(WiilConfigurationError):
        WillService(api_key="   ")


def test_will_service_validates_base_url():
    """WillService should reject invalid base URLs."""
    with pytest.raises(WiilConfigurationError):
        WillService(api_key="test-key", base_url="not-a-url")


def test_will_service_validates_timeout():
    """WillService should reject non-positive timeout values."""
    with pytest.raises(WiilConfigurationError):
        WillService(api_key="test-key", timeout=0)


def test_will_service_http_helpers_delegate(monkeypatch):
    """HTTP helper methods should delegate to underlying HttpClient."""
    service = WillService(api_key="test-key")

    monkeypatch.setattr(service._http, "get", lambda p, **k: ("get", p, k))
    monkeypatch.setattr(
        service._http,
        "post",
        lambda p, d, schema=None, **k: ("post", p, d, schema, k),
    )
    monkeypatch.setattr(
        service._http,
        "put",
        lambda p, d, schema=None, **k: ("put", p, d, schema, k),
    )
    monkeypatch.setattr(
        service._http,
        "patch",
        lambda p, d, schema=None, **k: ("patch", p, d, schema, k),
    )
    monkeypatch.setattr(
        service._http,
        "delete",
        lambda p, **k: ("delete", p, k),
    )

    assert service.get("/x") == ("get", "/x", {})
    assert service.post("/x", {"a": 1})[0] == "post"
    assert service.put("/x", {"a": 1})[0] == "put"
    assert service.patch("/x", {"a": 1})[0] == "patch"
    assert service.delete("/x") == ("delete", "/x", {})
