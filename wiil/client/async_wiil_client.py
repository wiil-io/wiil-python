"""Async WIIL SDK client.

This module provides an async facade over the existing synchronous WIIL SDK
resources. Resource method calls are executed in worker threads via
``asyncio.to_thread`` so consumers can use ``await`` and async context
managers.
"""

import asyncio
from typing import Any

from wiil.client.wiil_client import WiilClient


class _AsyncResourceProxy:
    """Async wrapper for a synchronous resource object."""

    def __init__(self, target: Any):
        self._target = target

    def __getattr__(self, name: str) -> Any:
        attribute = getattr(self._target, name)

        if callable(attribute):
            async def _async_call(*args: Any, **kwargs: Any) -> Any:
                return await asyncio.to_thread(attribute, *args, **kwargs)

            return _async_call

        return attribute


class AsyncWiilClient:
    """Async client for interacting with the WIIL Platform API.

    This client mirrors ``WiilClient`` properties while exposing resource
    method calls as awaitable coroutines.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.wiil.io/v1",
        timeout: int = 30,
    ):
        self._sync_client = WiilClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )

        for name, value in vars(self._sync_client).items():
            if name.startswith("_"):
                continue
            setattr(self, name, _AsyncResourceProxy(value))

    def __getattr__(self, name: str) -> Any:
        """Proxy any additional attributes to the underlying sync client."""
        attribute = getattr(self._sync_client, name)

        if callable(attribute):
            async def _async_call(*args: Any, **kwargs: Any) -> Any:
                return await asyncio.to_thread(attribute, *args, **kwargs)

            return _async_call

        return attribute

    async def aclose(self) -> None:
        """Close the underlying HTTP session."""
        await asyncio.to_thread(self._sync_client._http.session.close)

    async def __aenter__(self) -> "AsyncWiilClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()


__all__ = ["AsyncWiilClient"]
