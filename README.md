# OpenEC

**Open Source AI-Powered Ecommerce & Retail Analytics Platform**

OpenEC is a modular, extensible platform for ecommerce and retail data analytics — built for marketers, digital marketers, market analysts, pricing analysts, product managers, and anyone working in ecommerce. Inspired by [OpenBB](https://github.com/OpenBB-finance/OpenBB) for finance, OpenEC brings the same plugin-based, provider-agnostic architecture to the retail and ecommerce domain.

---

## Architecture

```
openEC/
├── openec_platform/           # Core platform
│   ├── core/                  # Router, command runner, provider interface, API
│   │   ├── router.py          # Decorator-based command registration
│   │   ├── command_runner.py  # Execution engine
│   │   ├── provider_interface.py  # Provider abstraction & registry
│   │   ├── oecject.py         # Universal response wrapper (OECject)
│   │   └── api.py             # FastAPI application factory
│   └── models/                # Standard data models per domain
│       ├── products.py        # ProductInfo, SalesHistorical, ProductRanking, ProductReview
│       ├── orders.py          # OrderSummary, OrderDetail, FulfillmentStatus, ReturnsSummary
│       ├── customers.py       # CustomerCohort, CustomerLifetimeValue, CustomerSegment, CustomerAcquisition
│       ├── inventory.py       # InventoryLevel, DemandForecast, StockMovement
│       ├── marketing.py       # CampaignPerformance, ChannelAttribution, KeywordPerformance
│       ├── analytics.py       # FunnelConversion, TrafficSource, CategoryPerformance
│       └── pricing.py         # PriceHistorical, CompetitorPrice, PriceElasticity
├── openec_extensions/         # Domain-specific command modules
│   ├── products.py            # /products/sales/*, /products/catalog/*, /products/rankings/*
│   ├── orders.py              # /orders/*, /orders/fulfillment/*, /orders/returns/*
│   ├── customers.py           # /customers/cohorts/*, /customers/ltv/*, /customers/segments/*
│   ├── inventory.py           # /inventory/levels/*, /inventory/forecasting/*
│   ├── marketing.py           # /marketing/campaigns/*, /marketing/attribution/*
│   ├── analytics.py           # /analytics/funnel/*, /analytics/traffic/*
│   └── pricing.py             # /pricing/history/*, /pricing/competitor/*, /pricing/optimization/*
├── openec_providers/          # Data source adapters
│   └── demo/                  # Built-in demo provider (mock data, no API keys needed)
├── openec_cli/                # CLI interface (Typer + Rich)
├── cookiecutter/              # Templates for creating new extensions & providers
└── pyproject.toml             # Project configuration (Poetry)
```

## Key Concepts

### Provider Pattern
One API, many data sources. Define a standard model once (e.g., `SalesHistorical`), then implement provider adapters for Shopify, Amazon SP-API, WooCommerce, Google Analytics, etc. Swap providers at query time:

```python
result = runner.run("/products/sales/historical", provider="shopify")
result = runner.run("/products/sales/historical", provider="amazon")
```

### OECject Response Wrapper
Every command returns an `OECject` with unified access methods:

```python
result.to_dataframe()   # pandas DataFrame
result.to_dict()        # dict / list of dicts
result.to_json()        # JSON string
result.to_chart()       # matplotlib/plotly chart
```

### Extension System
Add new domains or commands as pip-installable plugins, discovered at runtime via Python entry points.

## Command Hierarchy

| Domain | Routes | Use Cases |
|--------|--------|-----------|
| **Products** | `/products/sales/*`, `/products/catalog/*`, `/products/rankings/*`, `/products/reviews/*` | Sales analytics, catalog search, BSR tracking, review monitoring |
| **Orders** | `/orders/*`, `/orders/fulfillment/*`, `/orders/returns/*` | Order metrics, fulfillment tracking, returns analysis |
| **Customers** | `/customers/cohorts/*`, `/customers/ltv/*`, `/customers/segments/*`, `/customers/acquisition/*` | Retention analysis, LTV, RFM segmentation, CAC |
| **Inventory** | `/inventory/levels/*`, `/inventory/forecasting/*`, `/inventory/movements/*` | Stock management, demand forecasting, turnover |
| **Marketing** | `/marketing/campaigns/*`, `/marketing/attribution/*`, `/marketing/keywords/*` | Campaign ROI, attribution modeling, keyword analytics |
| **Analytics** | `/analytics/funnel/*`, `/analytics/traffic/*`, `/analytics/category/*` | Conversion funnels, traffic sources, category performance |
| **Pricing** | `/pricing/history/*`, `/pricing/competitor/*`, `/pricing/optimization/*` | Price tracking, competitor monitoring, elasticity analysis |

## Quick Start

```bash
# Install
pip install -e .

# List all commands
openec commands

# Run a command
openec run /products/sales/historical --provider demo --output table
openec run /inventory/levels/current --output json
openec run /marketing/campaigns/performance --output csv

# Start the REST API (port 6900)
openec api

# List providers
openec providers
```

## REST API

```bash
# Start server
openec api

# Endpoints
GET /                           # API info + all routes
GET /api/v1/commands            # List commands
GET /api/v1/products/sales/historical?provider=demo
GET /api/v1/inventory/levels/current?provider=demo
GET /docs                       # Swagger UI
GET /redoc                      # ReDoc
```

## Creating Custom Providers

Use the cookiecutter template or implement `ProviderFetcher`:

```python
from openec_platform.core.provider_interface import ProviderFetcher, ProviderInfo, QueryParams

class ShopifyProductsFetcher(ProviderFetcher):
    def fetch(self, params, **kwargs):
        # Call Shopify API
        return raw_data

    def transform(self, data, **kwargs):
        # Map to standard models
        return [SalesHistorical(**r) for r in data]

provider = ProviderInfo(name="shopify", description="Shopify store data")
provider.register_fetcher("SalesHistorical", ShopifyProductsFetcher())
```

## Target Users

- **Digital Marketers** - Campaign performance, attribution, keyword analytics
- **Market Analysts** - Category trends, market share, competitive intelligence
- **Pricing Analysts** - Price tracking, competitor monitoring, elasticity modeling
- **Product Managers** - Sales analytics, customer feedback, funnel optimization
- **Inventory Planners** - Stock levels, demand forecasting, turnover analysis
- **E-commerce Operators** - Order management, fulfillment tracking, returns analysis

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9-3.12 |
| API | FastAPI + Uvicorn |
| Data Validation | Pydantic v2 |
| CLI | Typer + Rich |
| Package Management | Poetry |
| Plugin Discovery | setuptools entry_points |
| Data Processing | pandas |

## Reference Links

- [OpenBB Platform](https://github.com/OpenBB-finance/OpenBB) - Inspiration for architecture and design patterns
- [OpenBB Website](https://openbb.co/) - Reference for product and UX approach
- [OpenBB Agents](https://github.com/OpenBB-finance/agents-for-openbb) - Reference for AI agent integration
- [OpenBB Finance GitHub](https://github.com/OpenBB-finance/) - Organization reference

## License

AGPL-3.0
