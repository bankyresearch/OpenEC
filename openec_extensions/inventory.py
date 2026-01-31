"""Inventory extension - commands for stock levels, demand forecasting, and movements."""

from openec_platform.core.router import Router

router = Router(prefix="/inventory")

levels_router = Router(prefix="/levels")
forecast_router = Router(prefix="/forecasting")
movement_router = Router(prefix="/movements")


@levels_router.command(model="InventoryLevel", description="Get current inventory levels")
def current(warehouse: str = "", provider: str = "demo"):
    """Current stock levels across warehouses."""
    pass


@levels_router.command(model="InventoryLevel", description="Get low stock alerts")
def alerts(threshold: int = 10, provider: str = "demo"):
    """Products at or below reorder point."""
    pass


@forecast_router.command(model="DemandForecast", description="Get demand forecast")
def demand(sku: str = "", category: str = "", horizon: str = "30d", provider: str = "demo"):
    """Demand forecasting for products or categories."""
    pass


@movement_router.command(model="StockMovement", description="Get stock movement history")
def history(sku: str = "", period: str = "30d", provider: str = "demo"):
    """Stock movement and turnover data."""
    pass


router.include_router(levels_router)
router.include_router(forecast_router)
router.include_router(movement_router)
