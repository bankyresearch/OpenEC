"""OECject - Universal response wrapper for all OpenEC commands.

Inspired by OpenBB's OBBject pattern. Every command returns an OECject,
providing a unified interface for data access, conversion, and visualization.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field

T = TypeVar("T")


class OECject(BaseModel, Generic[T]):
    """Universal response object returned by all OpenEC commands.

    Attributes:
        results: The raw data returned by the provider.
        provider: Name of the provider that supplied the data.
        model: The standard model name used for the query.
        command: The command path that produced this result.
        timestamp: When the result was generated.
        warnings: Any warnings from the provider or validation.
        extra: Provider-specific metadata.
    """

    results: Optional[T] = None
    provider: str = ""
    model: str = ""
    command: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)
    extra: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}

    def to_dict(self) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """Convert results to a dictionary or list of dictionaries."""
        if self.results is None:
            return None
        if isinstance(self.results, list):
            return [
                item.model_dump() if isinstance(item, BaseModel) else item
                for item in self.results
            ]
        if isinstance(self.results, BaseModel):
            return self.results.model_dump()
        return self.results

    def to_dataframe(self) -> Any:
        """Convert results to a pandas DataFrame."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required: pip install pandas")

        data = self.to_dict()
        if data is None:
            return pd.DataFrame()
        if isinstance(data, list):
            return pd.DataFrame(data)
        return pd.DataFrame([data])

    def to_json(self, indent: int = 2) -> str:
        """Serialize the full response to JSON."""
        return self.model_dump_json(indent=indent)

    def to_chart(self, **kwargs: Any) -> Any:
        """Generate a chart from the results (requires matplotlib or plotly)."""
        df = self.to_dataframe()
        if df.empty:
            raise ValueError("No data to chart.")
        try:
            return df.plot(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Charting failed: {e}")

    def __repr__(self) -> str:
        count = len(self.results) if isinstance(self.results, list) else (1 if self.results else 0)
        return (
            f"OECject(provider={self.provider!r}, model={self.model!r}, "
            f"records={count}, command={self.command!r})"
        )
