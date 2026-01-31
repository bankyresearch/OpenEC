"""Standard models for product-related data."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class ProductInfo(StandardModel):
    """Canonical product information."""

    sku: str
    name: str
    category: str = ""
    subcategory: str = ""
    brand: str = ""
    price: float = 0.0
    currency: str = "USD"
    status: str = "active"
    marketplace: str = ""
    url: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: int = 0
    attributes: Dict[str, Any] = {}


class SalesHistorical(StandardModel):
    """Historical sales data for a product or category."""

    date: date
    sku: str = ""
    name: str = ""
    units_sold: int = 0
    revenue: float = 0.0
    currency: str = "USD"
    marketplace: str = ""
    category: str = ""
    average_selling_price: float = 0.0
    returns: int = 0
    net_units: int = 0


class ProductRanking(StandardModel):
    """Product ranking / best seller rank data."""

    date: date
    sku: str
    name: str = ""
    rank: int = 0
    category: str = ""
    marketplace: str = ""
    change: int = 0  # rank change from previous period


class ProductReview(StandardModel):
    """Product review / rating data."""

    date: date
    sku: str
    rating: float
    title: str = ""
    body: str = ""
    verified_purchase: bool = False
    marketplace: str = ""
    helpful_votes: int = 0
