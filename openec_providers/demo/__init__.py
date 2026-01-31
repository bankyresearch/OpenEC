"""Demo provider - generates realistic mock data for all OpenEC domains.

This provider is used for development, testing, and demonstration purposes.
It requires no API keys or external services.
"""

from openec_platform.core.provider_interface import ProviderInfo
from openec_providers.demo.fetchers import (
    DemoAnalyticsFetcher,
    DemoCustomersFetcher,
    DemoInventoryFetcher,
    DemoMarketingFetcher,
    DemoOrdersFetcher,
    DemoPricingFetcher,
    DemoProductsFetcher,
)

provider = ProviderInfo(
    name="demo",
    description="Demo provider with realistic mock ecommerce data",
    website="https://github.com/bankyresearch/openEC",
    credentials=[],
    fetchers={},
)

# Register all fetchers
_fetcher_map = {
    # Products
    "ProductInfo": DemoProductsFetcher(),
    "SalesHistorical": DemoProductsFetcher(),
    "ProductRanking": DemoProductsFetcher(),
    "ProductReview": DemoProductsFetcher(),
    # Orders
    "OrderSummary": DemoOrdersFetcher(),
    "OrderDetail": DemoOrdersFetcher(),
    "FulfillmentStatus": DemoOrdersFetcher(),
    "ReturnsSummary": DemoOrdersFetcher(),
    # Customers
    "CustomerCohort": DemoCustomersFetcher(),
    "CustomerLifetimeValue": DemoCustomersFetcher(),
    "CustomerSegment": DemoCustomersFetcher(),
    "CustomerAcquisition": DemoCustomersFetcher(),
    # Inventory
    "InventoryLevel": DemoInventoryFetcher(),
    "DemandForecast": DemoInventoryFetcher(),
    "StockMovement": DemoInventoryFetcher(),
    # Marketing
    "CampaignPerformance": DemoMarketingFetcher(),
    "ChannelAttribution": DemoMarketingFetcher(),
    "KeywordPerformance": DemoMarketingFetcher(),
    # Analytics
    "FunnelConversion": DemoAnalyticsFetcher(),
    "TrafficSource": DemoAnalyticsFetcher(),
    "CategoryPerformance": DemoAnalyticsFetcher(),
    # Pricing
    "PriceHistorical": DemoPricingFetcher(),
    "CompetitorPrice": DemoPricingFetcher(),
    "PriceElasticity": DemoPricingFetcher(),
}

for model_name, fetcher in _fetcher_map.items():
    provider.register_fetcher(model_name, fetcher)
