"""Standard models for pricing and competitor intelligence."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class PriceHistorical(StandardModel):
    """Historical price tracking."""

    date: date
    sku: str
    name: str = ""
    price: float = 0.0
    currency: str = "USD"
    marketplace: str = ""
    seller: str = ""
    is_deal: bool = False
    discount_pct: float = 0.0


class CompetitorPrice(StandardModel):
    """Competitor pricing data."""

    date: date
    sku: str = ""
    product_name: str = ""
    competitor: str = ""
    price: float = 0.0
    currency: str = "USD"
    marketplace: str = ""
    url: Optional[str] = None
    in_stock: bool = True
    price_difference: float = 0.0  # vs your price
    price_difference_pct: float = 0.0


class PriceElasticity(StandardModel):
    """Price elasticity analysis."""

    sku: str = ""
    category: str = ""
    elasticity: float = 0.0  # % change in demand / % change in price
    optimal_price: float = 0.0
    current_price: float = 0.0
    currency: str = "USD"
    confidence: float = 0.0
    sample_size: int = 0
