"""Standard models for web/store analytics data."""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class FunnelConversion(StandardModel):
    """Conversion funnel data."""

    date: date
    stage: str  # visit, product_view, add_to_cart, checkout, purchase
    users: int = 0
    conversion_rate: float = 0.0
    drop_off_rate: float = 0.0
    marketplace: str = ""


class TrafficSource(StandardModel):
    """Traffic source breakdown."""

    date: date
    source: str  # organic, paid, direct, social, email, referral
    sessions: int = 0
    users: int = 0
    bounce_rate: float = 0.0
    pages_per_session: float = 0.0
    avg_session_duration: float = 0.0  # seconds
    conversions: int = 0
    revenue: float = 0.0
    currency: str = "USD"


class CategoryPerformance(StandardModel):
    """Performance metrics by product category."""

    date: date
    category: str
    subcategory: str = ""
    views: int = 0
    units_sold: int = 0
    revenue: float = 0.0
    conversion_rate: float = 0.0
    average_price: float = 0.0
    currency: str = "USD"
    market_share: float = 0.0
