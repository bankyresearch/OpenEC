"""Standard models for inventory-related data."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class InventoryLevel(StandardModel):
    """Current inventory snapshot."""

    sku: str
    name: str = ""
    quantity: int = 0
    warehouse: str = ""
    status: str = "in_stock"  # in_stock, low_stock, out_of_stock
    reorder_point: int = 0
    days_of_supply: float = 0.0
    last_updated: Optional[datetime] = None


class DemandForecast(StandardModel):
    """Demand forecasting data."""

    date: date
    sku: str = ""
    category: str = ""
    predicted_demand: float = 0.0
    lower_bound: float = 0.0
    upper_bound: float = 0.0
    confidence: float = 0.0
    method: str = ""


class StockMovement(StandardModel):
    """Stock movement / turnover data."""

    date: date
    sku: str
    name: str = ""
    received: int = 0
    sold: int = 0
    returned: int = 0
    adjusted: int = 0
    closing_stock: int = 0
    turnover_rate: float = 0.0
