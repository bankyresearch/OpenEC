"""Provider abstraction layer for OpenEC.

Defines the contracts that data providers must implement.
Providers are discovered at runtime via Python entry points.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import BaseModel


class StandardModel(BaseModel):
    """Base class for all standard data models.

    Standard models define the canonical schema for a data type.
    Providers map their raw data into these models.
    """

    class Config:
        extra = "allow"


class QueryParams(BaseModel):
    """Base class for query parameters passed to provider fetchers."""

    provider: str = "demo"


class ProviderFetcher(ABC):
    """Abstract base for a single data fetcher within a provider.

    Each fetcher handles one standard model (e.g., SalesHistorical).
    """

    @abstractmethod
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        """Fetch data from the source and return raw records."""
        ...

    @abstractmethod
    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        """Transform raw records into standard model instances."""
        ...


@dataclass
class ProviderInfo:
    """Metadata and registry for a single provider."""

    name: str
    description: str = ""
    website: str = ""
    credentials: List[str] = field(default_factory=list)
    fetchers: Dict[str, ProviderFetcher] = field(default_factory=dict)

    def register_fetcher(self, model_name: str, fetcher: ProviderFetcher) -> None:
        """Register a fetcher for a given standard model."""
        self.fetchers[model_name] = fetcher


class ProviderRegistry:
    """Central registry for all available data providers.

    Providers register themselves here, either manually or via entry points.
    The command runner uses this registry to route queries to the correct provider.
    """

    def __init__(self) -> None:
        self._providers: Dict[str, ProviderInfo] = {}

    def register(self, provider: ProviderInfo) -> None:
        """Register a provider."""
        self._providers[provider.name] = provider

    def get(self, name: str) -> ProviderInfo:
        """Get a provider by name."""
        if name not in self._providers:
            available = ", ".join(sorted(self._providers.keys()))
            raise KeyError(f"Provider '{name}' not found. Available: {available}")
        return self._providers[name]

    def list_providers(self) -> List[str]:
        """List all registered provider names."""
        return sorted(self._providers.keys())

    def get_fetcher(self, provider_name: str, model_name: str) -> ProviderFetcher:
        """Get a specific fetcher from a provider."""
        provider = self.get(provider_name)
        if model_name not in provider.fetchers:
            available = ", ".join(sorted(provider.fetchers.keys()))
            raise KeyError(
                f"Provider '{provider_name}' has no fetcher for '{model_name}'. "
                f"Available: {available}"
            )
        return provider.fetchers[model_name]

    def discover_entry_points(self, group: str = "openec_core_provider") -> None:
        """Auto-discover providers from installed Python entry points."""
        try:
            from importlib.metadata import entry_points

            eps = entry_points()
            # Python 3.12+ returns a SelectableGroups, 3.9+ returns dict
            if isinstance(eps, dict):
                provider_eps = eps.get(group, [])
            else:
                provider_eps = eps.select(group=group) if hasattr(eps, "select") else []

            for ep in provider_eps:
                try:
                    provider = ep.load()
                    if isinstance(provider, ProviderInfo):
                        self.register(provider)
                except Exception:
                    pass
        except ImportError:
            pass


# Global registry instance
registry = ProviderRegistry()
