"""Standard models for marketing and advertising data."""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from openec_platform.core.provider_interface import StandardModel


class CampaignPerformance(StandardModel):
    """Marketing campaign performance metrics."""

    date: date
    campaign_id: str = ""
    campaign_name: str = ""
    channel: str = ""  # google_ads, meta, tiktok, email, etc.
    impressions: int = 0
    clicks: int = 0
    ctr: float = 0.0
    spend: float = 0.0
    conversions: int = 0
    revenue: float = 0.0
    roas: float = 0.0  # return on ad spend
    cpc: float = 0.0
    cpa: float = 0.0
    currency: str = "USD"


class ChannelAttribution(StandardModel):
    """Marketing channel attribution data."""

    date: date
    channel: str
    first_touch_conversions: int = 0
    last_touch_conversions: int = 0
    linear_conversions: float = 0.0
    revenue: float = 0.0
    assisted_conversions: int = 0
    currency: str = "USD"


class KeywordPerformance(StandardModel):
    """Search keyword / SEO performance."""

    date: date
    keyword: str
    search_volume: int = 0
    position: float = 0.0
    clicks: int = 0
    impressions: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    marketplace: str = ""
