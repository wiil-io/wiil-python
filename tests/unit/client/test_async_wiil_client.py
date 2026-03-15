"""Tests for AsyncWiilClient."""

import pytest

from wiil.client.async_wiil_client import AsyncWiilClient


class _DummySession:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class _DummyHTTP:
    def __init__(self):
        self.session = _DummySession()


class _DummyResource:
    label = "resource-label"

    def greet(self, name: str) -> str:
        return f"hello {name}"

    def fail(self) -> None:
        raise ValueError("boom")


class _DummyWiilClient:
    def __init__(self, api_key: str, base_url: str, timeout: int):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.organizations = _DummyResource()
        self._http = _DummyHTTP()


@pytest.mark.asyncio
async def test_async_client_proxies_resource_methods(monkeypatch):
    """Async wrapper should await sync resource method calls."""
    monkeypatch.setattr(
        "wiil.client.async_wiil_client.WiilClient",
        _DummyWiilClient,
    )

    client = AsyncWiilClient(api_key="key")
    result = await client.organizations.greet("world")

    assert result == "hello world"
    assert client.organizations.label == "resource-label"


@pytest.mark.asyncio
async def test_async_client_context_manager_closes_session(monkeypatch):
    """Async context manager should close underlying session."""
    monkeypatch.setattr(
        "wiil.client.async_wiil_client.WiilClient",
        _DummyWiilClient,
    )

    async with AsyncWiilClient(api_key="key") as client:
        assert await client.organizations.greet("team") == "hello team"

    assert client._sync_client._http.session.closed is True


@pytest.mark.asyncio
async def test_async_client_propagates_method_errors(monkeypatch):
    """Errors from sync methods should propagate through async proxy."""
    monkeypatch.setattr(
        "wiil.client.async_wiil_client.WiilClient",
        _DummyWiilClient,
    )

    client = AsyncWiilClient(api_key="key")

    with pytest.raises(ValueError, match="boom"):
        await client.organizations.fail()
