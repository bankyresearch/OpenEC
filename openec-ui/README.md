# OpenEC UI

**Web Dashboard for OpenEC - Ecommerce & Retail Analytics**

OpenEC UI is a React-based web dashboard that provides interactive visualizations and data tables for the [OpenEC](https://pypi.org/project/openec/) analytics platform. Install it with pip, run one command, and access a full analytics dashboard in your browser.

---

## Prerequisites

- **Python 3.9 - 3.12**
- **openec** (`pip install openec`) - the core analytics engine (installed automatically as a dependency)

## Installation

```bash
pip install openec-ui
```

This installs the dashboard along with all dependencies including `openec`, `uvicorn`, `typer`, and `rich`.

## Quick Start

```bash
# Start the dashboard (default: http://0.0.0.0:6900)
openec-ui

# Custom host and port
openec-ui --host 127.0.0.1 --port 8080
```

Open your browser to `http://localhost:6900` to access the dashboard.

## Dashboard Pages

| Page | Route | Description |
|------|-------|-------------|
| **Overview** | `/` | KPI summary, revenue trends, sales by category, marketing spend vs revenue, inventory status |
| **Products** | `/products` | Product performance, daily units sold, revenue by product, sales data table |
| **Orders** | `/orders` | Order metrics, revenue trends, average order value, cancellations and returns |
| **Customers** | `/customers` | Customer segmentation, RFM analysis, segment distribution |
| **Inventory** | `/inventory` | Stock levels by warehouse, low stock alerts, inventory status breakdown |
| **Marketing** | `/marketing` | Campaign performance, spend vs revenue, ROAS by channel |
| **Analytics** | `/analytics` | Conversion funnel, daily visitors trend, funnel stage analysis |
| **Pricing** | `/pricing` | Competitor price comparison, price difference distribution, stock tracking |

## How It Works

OpenEC UI bundles a pre-built React single-page application (SPA) inside the pip package. When you run `openec-ui`, it starts a FastAPI server that:

1. **Serves the React dashboard** at the root URL (`/`)
2. **Mounts the OpenEC API** at `/api` so the frontend can fetch analytics data
3. **Provides Swagger docs** at `/docs` for API exploration

The dashboard fetches data from the OpenEC API using the provider system. By default, the built-in `demo` provider returns mock data so you can explore the dashboard immediately without any external API keys or data sources.

```
Browser (React SPA)
  |
  |--> GET /api/api/v1/sales/historical?provider=demo
  |--> GET /api/api/v1/orders/summary?provider=demo
  |--> GET /api/api/v1/campaigns/performance?provider=demo
  |
FastAPI Server (openec-ui)
  |
  |--> OpenEC Core (command runner + router + providers)
```

## Using Custom Providers

If you have custom OpenEC providers installed (e.g., Shopify, Amazon, WooCommerce), you can switch providers directly from the dashboard using the provider selector in the header.

```bash
# Install a custom provider
pip install openec-provider-shopify

# Start the dashboard - your provider will appear in the dropdown
openec-ui
```

## API Documentation

While the dashboard is running, access the interactive API docs:

- **Swagger UI**: `http://localhost:6900/docs`
- **All endpoints**: `http://localhost:6900/api/docs`

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript 5 |
| Build Tool | Vite 5 |
| Charts | Chart.js 4 + react-chartjs-2 |
| Styling | Tailwind CSS 3 |
| Icons | Lucide React |
| Routing | React Router 6 |
| Backend | FastAPI + Uvicorn |
| CLI | Typer + Rich |

## Development

To modify the frontend and rebuild:

```bash
# Clone the repo
git clone https://github.com/bankyresearch/OpenEC.git
cd OpenEC/openec-ui/frontend

# Install dependencies
npm install

# Dev server (with hot reload, proxies API to localhost:6900)
npm run dev

# Production build (outputs to ../openec_ui/static/)
npm run build
```

For frontend development, run the OpenEC API server separately:

```bash
# Terminal 1: Start the backend API
openec api

# Terminal 2: Start Vite dev server (auto-proxies to backend)
cd openec-ui/frontend && npm run dev
```

## License

AGPL-3.0
