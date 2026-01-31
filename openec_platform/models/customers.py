"""Standard models for customer-related data."""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class CustomerCohort(StandardModel):
    """Customer cohort retention analysis."""

    cohort_date: date
    period: int = 0  # months since acquisition
    cohort_size: int = 0
    retained: int = 0
    retention_rate: float = 0.0
    revenue: float = 0.0
    currency: str = "USD"


class CustomerLifetimeValue(StandardModel):
    """Customer lifetime value metrics."""

    segment: str = ""
    average_ltv: float = 0.0
    median_ltv: float = 0.0
    average_order_frequency: float = 0.0
    average_order_value: float = 0.0
    average_lifespan_days: int = 0
    currency: str = "USD"
    customer_count: int = 0


class CustomerSegment(StandardModel):
    """Customer segmentation data (RFM or custom)."""

    segment: str
    customer_count: int = 0
    percentage: float = 0.0
    avg_recency_days: float = 0.0
    avg_frequency: float = 0.0
    avg_monetary: float = 0.0
    currency: str = "USD"


class CustomerAcquisition(StandardModel):
    """Customer acquisition metrics by channel."""

    date: date
    channel: str = ""
    new_customers: int = 0
    cost: float = 0.0
    cac: float = 0.0  # customer acquisition cost
    currency: str = "USD"
    conversion_rate: float = 0.0
