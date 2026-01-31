"""Products extension - commands for product catalog, sales, rankings, and reviews."""

from openec_platform.core.router import Router

router = Router(prefix="/products")

sales_router = Router(prefix="/sales")
catalog_router = Router(prefix="/catalog")
rankings_router = Router(prefix="/rankings")
reviews_router = Router(prefix="/reviews")


@sales_router.command(model="SalesHistorical", description="Get historical sales data for a product or category")
def historical(sku: str = "", category: str = "", provider: str = "demo"):
    """Historical sales data by SKU or category."""
    pass


@sales_router.command(model="SalesHistorical", description="Get sales summary for a time period")
def summary(period: str = "30d", provider: str = "demo"):
    """Aggregated sales summary."""
    pass


@catalog_router.command(model="ProductInfo", description="Search the product catalog")
def search(query: str = "", category: str = "", provider: str = "demo"):
    """Search products by keyword or category."""
    pass


@catalog_router.command(model="ProductInfo", description="Get product details by SKU")
def details(sku: str = "", provider: str = "demo"):
    """Get detailed product information."""
    pass


@rankings_router.command(model="ProductRanking", description="Get best seller rankings")
def bestsellers(category: str = "", marketplace: str = "", provider: str = "demo"):
    """Best seller rankings by category."""
    pass


@reviews_router.command(model="ProductReview", description="Get product reviews and ratings")
def recent(sku: str = "", provider: str = "demo"):
    """Recent product reviews."""
    pass


@reviews_router.command(model="ProductReview", description="Get review sentiment analysis")
def sentiment(sku: str = "", provider: str = "demo"):
    """Review sentiment breakdown."""
    pass


router.include_router(sales_router)
router.include_router(catalog_router)
router.include_router(rankings_router)
router.include_router(reviews_router)
