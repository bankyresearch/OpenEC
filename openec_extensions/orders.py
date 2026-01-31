"""Orders extension - commands for order management, fulfillment, and returns."""

from openec_platform.core.router import Router

router = Router(prefix="/orders")

fulfillment_router = Router(prefix="/fulfillment")
returns_router = Router(prefix="/returns")


@router.command(model="OrderSummary", description="Get order summary metrics")
def summary(period: str = "30d", provider: str = "demo"):
    """Aggregated order summary for a period."""
    pass


@router.command(model="OrderDetail", description="Get recent orders")
def recent(limit: int = 50, provider: str = "demo"):
    """List recent orders."""
    pass


@fulfillment_router.command(model="FulfillmentStatus", description="Get fulfillment status breakdown")
def status(period: str = "7d", provider: str = "demo"):
    """Fulfillment status overview."""
    pass


@returns_router.command(model="ReturnsSummary", description="Get returns summary and trends")
def summary(period: str = "30d", provider: str = "demo"):
    """Returns and refunds summary."""
    pass


@returns_router.command(model="ReturnsSummary", description="Get top return reasons")
def reasons(period: str = "30d", provider: str = "demo"):
    """Top return reasons analysis."""
    pass


router.include_router(fulfillment_router)
router.include_router(returns_router)
