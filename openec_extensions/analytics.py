"""Analytics extension - commands for funnel, traffic, and category analytics."""

from openec_platform.core.router import Router

router = Router(prefix="/analytics")

funnel_router = Router(prefix="/funnel")
traffic_router = Router(prefix="/traffic")
category_router = Router(prefix="/category")


@funnel_router.command(model="FunnelConversion", description="Get conversion funnel data")
def conversion(period: str = "30d", provider: str = "demo"):
    """Full conversion funnel analysis."""
    pass


@funnel_router.command(model="FunnelConversion", description="Get cart abandonment metrics")
def abandonment(period: str = "30d", provider: str = "demo"):
    """Cart abandonment rates and trends."""
    pass


@traffic_router.command(model="TrafficSource", description="Get traffic source breakdown")
def sources(period: str = "30d", provider: str = "demo"):
    """Traffic sources and engagement metrics."""
    pass


@category_router.command(model="CategoryPerformance", description="Get category performance metrics")
def performance(category: str = "", provider: str = "demo"):
    """Category-level performance analysis."""
    pass


@category_router.command(model="CategoryPerformance", description="Get category market share")
def market_share(category: str = "", provider: str = "demo"):
    """Market share by category."""
    pass


router.include_router(funnel_router)
router.include_router(traffic_router)
router.include_router(category_router)
