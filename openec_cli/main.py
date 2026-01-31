"""OpenEC CLI - Command-line interface for the OpenEC platform.

Usage:
    openec products sales historical --sku EC-1001
    openec inventory levels current
    openec marketing campaigns performance
    openec api  # Start the REST API server
"""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="openec",
    help="OpenEC - Open Source AI-Powered Ecommerce & Retail Analytics Platform",
    no_args_is_help=True,
)
console = Console()


def _get_runner():
    """Build the command runner with all extensions loaded."""
    from openec_platform.core.command_runner import CommandRunner
    from openec_platform.core.provider_interface import registry
    from openec_platform.core.router import Router

    # Import extensions to register routes
    from openec_extensions import products, orders, customers, inventory, marketing, analytics, pricing

    # Import demo provider to register fetchers
    from openec_providers.demo import provider as demo_provider
    registry.register(demo_provider)

    # Build root router
    root = Router()
    root.include_router(products.router)
    root.include_router(orders.router)
    root.include_router(customers.router)
    root.include_router(inventory.router)
    root.include_router(marketing.router)
    root.include_router(analytics.router)
    root.include_router(pricing.router)

    return CommandRunner(root), root


@app.command()
def commands():
    """List all available commands."""
    runner, _ = _get_runner()
    table = Table(title="OpenEC Commands")
    table.add_column("Command Path", style="cyan")
    for cmd in runner.list_commands():
        table.add_row(cmd)
    console.print(table)


@app.command()
def run(
    path: str = typer.Argument(..., help="Command path (e.g., /products/sales/historical)"),
    provider: str = typer.Option("demo", "--provider", "-p", help="Data provider"),
    output: str = typer.Option("table", "--output", "-o", help="Output format: table, json, csv"),
):
    """Execute an OpenEC command."""
    runner, _ = _get_runner()

    try:
        result = runner.run(path, provider=provider)
    except KeyError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    if output == "json":
        console.print(result.to_json())
    elif output == "csv":
        df = result.to_dataframe()
        console.print(df.to_csv(index=False))
    else:
        df = result.to_dataframe()
        if df.empty:
            console.print("[yellow]No data returned.[/yellow]")
            return
        table = Table(title=f"{path} (provider: {provider})")
        for col in df.columns:
            table.add_column(str(col))
        for _, row in df.head(20).iterrows():
            table.add_row(*[str(v) for v in row])
        if len(df) > 20:
            console.print(f"[dim]Showing 20 of {len(df)} records[/dim]")
        console.print(table)


@app.command()
def api(
    host: str = typer.Option("0.0.0.0", help="API host"),
    port: int = typer.Option(6900, help="API port"),
):
    """Start the OpenEC REST API server."""
    import uvicorn
    from openec_platform.core.api import create_app

    _, root = _get_runner()
    fastapi_app = create_app(root)
    console.print(f"[green]Starting OpenEC API at http://{host}:{port}[/green]")
    console.print(f"[dim]Swagger docs: http://{host}:{port}/docs[/dim]")
    uvicorn.run(fastapi_app, host=host, port=port)


@app.command()
def providers():
    """List available data providers."""
    from openec_platform.core.provider_interface import registry
    from openec_providers.demo import provider as demo_provider
    registry.register(demo_provider)

    table = Table(title="Available Providers")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Models", style="green")

    for name in registry.list_providers():
        p = registry.get(name)
        models = ", ".join(sorted(p.fetchers.keys()))
        table.add_row(p.name, p.description, models)
    console.print(table)


if __name__ == "__main__":
    app()
