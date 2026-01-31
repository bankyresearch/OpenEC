"""Standard models for order-related data."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class OrderSummary(StandardModel):
    """Aggregated order summary data."""

    date: date
    total_orders: int = 0
    total_revenue: float = 0.0
    average_order_value: float = 0.0
    currency: str = "USD"
    marketplace: str = ""
    total_units: int = 0
    cancelled_orders: int = 0
    returned_orders: int = 0


class OrderDetail(StandardModel):
    """Individual order detail."""

    order_id: str
    date: datetime
    status: str = ""
    total: float = 0.0
    currency: str = "USD"
    items: int = 0
    marketplace: str = ""
    customer_id: str = ""
    shipping_method: str = ""
    payment_method: str = ""


class FulfillmentStatus(StandardModel):
    """Order fulfillment tracking."""

    date: date
    total_orders: int = 0
    pending: int = 0
    processing: int = 0
    shipped: int = 0
    delivered: int = 0
    cancelled: int = 0
    returned: int = 0
    fulfillment_rate: float = 0.0


class ReturnsSummary(StandardModel):
    """Returns and refunds summary."""

    date: date
    total_returns: int = 0
    return_rate: float = 0.0
    total_refunds: float = 0.0
    currency: str = "USD"
    top_return_reasons: List[str] = []
    marketplace: str = ""
