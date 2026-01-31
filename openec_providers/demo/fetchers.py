"""Demo data fetchers - generate realistic mock ecommerce data."""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from openec_platform.core.provider_interface import ProviderFetcher, QueryParams, StandardModel

# Seed for reproducibility
random.seed(42)

DEMO_PRODUCTS = [
    {"sku": "EC-1001", "name": "Wireless Bluetooth Headphones", "category": "Electronics", "brand": "SoundMax", "price": 79.99},
    {"sku": "EC-1002", "name": "Organic Cotton T-Shirt", "category": "Apparel", "brand": "EcoWear", "price": 29.99},
    {"sku": "EC-1003", "name": "Stainless Steel Water Bottle", "category": "Home & Kitchen", "brand": "HydroFlow", "price": 24.99},
    {"sku": "EC-1004", "name": "Running Shoes Pro", "category": "Sports", "brand": "SprintX", "price": 129.99},
    {"sku": "EC-1005", "name": "Vitamin C Serum", "category": "Beauty", "brand": "GlowUp", "price": 34.99},
    {"sku": "EC-1006", "name": "Mechanical Keyboard RGB", "category": "Electronics", "brand": "TypeMaster", "price": 89.99},
    {"sku": "EC-1007", "name": "Yoga Mat Premium", "category": "Sports", "brand": "ZenFit", "price": 49.99},
    {"sku": "EC-1008", "name": "Coffee Grinder Electric", "category": "Home & Kitchen", "brand": "BrewPerfect", "price": 59.99},
    {"sku": "EC-1009", "name": "Kids Building Blocks Set", "category": "Toys", "brand": "BrainBuild", "price": 39.99},
    {"sku": "EC-1010", "name": "Phone Case Ultra Slim", "category": "Electronics", "brand": "ShieldPro", "price": 19.99},
]

CHANNELS = ["google_ads", "meta_ads", "tiktok_ads", "email", "organic", "direct", "referral"]
MARKETPLACES = ["amazon", "shopify", "walmart", "ebay"]


def _date_range(days: int = 30) -> List[date]:
    today = date.today()
    return [today - timedelta(days=i) for i in range(days, 0, -1)]


class DemoProductsFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        records = []
        for d in _date_range(30):
            for p in DEMO_PRODUCTS:
                units = random.randint(5, 200)
                records.append({
                    "date": d.isoformat(),
                    "sku": p["sku"],
                    "name": p["name"],
                    "category": p["category"],
                    "brand": p["brand"],
                    "price": p["price"],
                    "units_sold": units,
                    "revenue": round(units * p["price"], 2),
                    "marketplace": random.choice(MARKETPLACES),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "review_count": random.randint(10, 500),
                })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.products import SalesHistorical
        return [SalesHistorical(**r) for r in data]


class DemoOrdersFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        records = []
        for d in _date_range(30):
            orders = random.randint(50, 500)
            revenue = round(orders * random.uniform(35, 120), 2)
            records.append({
                "date": d.isoformat(),
                "total_orders": orders,
                "total_revenue": revenue,
                "average_order_value": round(revenue / orders, 2),
                "total_units": int(orders * random.uniform(1.5, 3.0)),
                "cancelled_orders": random.randint(0, int(orders * 0.05)),
                "returned_orders": random.randint(0, int(orders * 0.08)),
                "marketplace": random.choice(MARKETPLACES),
            })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.orders import OrderSummary
        return [OrderSummary(**r) for r in data]


class DemoCustomersFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        segments = ["Champions", "Loyal", "Potential Loyalists", "New Customers", "At Risk", "Lost"]
        records = []
        total = 10000
        for seg in segments:
            count = random.randint(500, 3000)
            records.append({
                "segment": seg,
                "customer_count": count,
                "percentage": round(count / total * 100, 1),
                "avg_recency_days": round(random.uniform(1, 180), 1),
                "avg_frequency": round(random.uniform(1, 20), 1),
                "avg_monetary": round(random.uniform(20, 500), 2),
            })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.customers import CustomerSegment
        return [CustomerSegment(**r) for r in data]


class DemoInventoryFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        records = []
        warehouses = ["US-East", "US-West", "EU-Central"]
        for p in DEMO_PRODUCTS:
            for wh in warehouses:
                qty = random.randint(0, 500)
                records.append({
                    "sku": p["sku"],
                    "name": p["name"],
                    "quantity": qty,
                    "warehouse": wh,
                    "status": "out_of_stock" if qty == 0 else ("low_stock" if qty < 20 else "in_stock"),
                    "reorder_point": 20,
                    "days_of_supply": round(qty / max(random.uniform(2, 15), 0.1), 1),
                })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.inventory import InventoryLevel
        return [InventoryLevel(**r) for r in data]


class DemoMarketingFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        records = []
        for d in _date_range(30):
            for ch in CHANNELS[:4]:  # paid channels
                impressions = random.randint(5000, 100000)
                clicks = int(impressions * random.uniform(0.01, 0.08))
                spend = round(clicks * random.uniform(0.5, 3.0), 2)
                conversions = int(clicks * random.uniform(0.02, 0.1))
                revenue = round(conversions * random.uniform(40, 150), 2)
                records.append({
                    "date": d.isoformat(),
                    "channel": ch,
                    "impressions": impressions,
                    "clicks": clicks,
                    "ctr": round(clicks / impressions * 100, 2),
                    "spend": spend,
                    "conversions": conversions,
                    "revenue": revenue,
                    "roas": round(revenue / spend, 2) if spend > 0 else 0,
                    "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
                    "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
                })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.marketing import CampaignPerformance
        return [CampaignPerformance(**r) for r in data]


class DemoAnalyticsFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        stages = ["visit", "product_view", "add_to_cart", "checkout", "purchase"]
        records = []
        for d in _date_range(30):
            users = random.randint(5000, 20000)
            for i, stage in enumerate(stages):
                users = int(users * random.uniform(0.3, 0.7)) if i > 0 else users
                records.append({
                    "date": d.isoformat(),
                    "stage": stage,
                    "users": users,
                    "conversion_rate": 100.0 if i == 0 else round(random.uniform(20, 70), 1),
                    "drop_off_rate": 0.0 if i == 0 else round(random.uniform(30, 80), 1),
                })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.analytics import FunnelConversion
        return [FunnelConversion(**r) for r in data]


class DemoPricingFetcher(ProviderFetcher):
    def fetch(self, params: QueryParams, **kwargs: Any) -> List[Dict[str, Any]]:
        competitors = ["CompetitorA", "CompetitorB", "CompetitorC"]
        records = []
        for d in _date_range(30):
            for p in DEMO_PRODUCTS[:5]:
                for comp in competitors:
                    comp_price = round(p["price"] * random.uniform(0.8, 1.2), 2)
                    records.append({
                        "date": d.isoformat(),
                        "sku": p["sku"],
                        "product_name": p["name"],
                        "competitor": comp,
                        "price": comp_price,
                        "marketplace": random.choice(MARKETPLACES),
                        "in_stock": random.random() > 0.1,
                        "price_difference": round(comp_price - p["price"], 2),
                        "price_difference_pct": round((comp_price - p["price"]) / p["price"] * 100, 1),
                    })
        return records

    def transform(self, data: List[Dict[str, Any]], **kwargs: Any) -> List[StandardModel]:
        from openec_platform.models.pricing import CompetitorPrice
        return [CompetitorPrice(**r) for r in data]
