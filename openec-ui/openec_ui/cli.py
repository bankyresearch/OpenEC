"""CLI entry point for the OpenEC dashboard."""

import typer
from rich.console import Console

app = typer.Typer(help="OpenEC Dashboard - Web UI for ecommerce analytics")
console = Console()


@app.callback(invoke_without_command=True)
def main(
    host: str = typer.Option("0.0.0.0", help="Server host"),
    port: int = typer.Option(6900, help="Server port"),
):
    """Start the OpenEC dashboard server."""
    import uvicorn
    from openec_ui.server import create_app

    dashboard_app = create_app()
    console.print(f"[bold green]OpenEC Dashboard[/bold green]")
    console.print(f"[green]Dashboard: http://{host}:{port}[/green]")
    console.print(f"[dim]API docs:  http://{host}:{port}/docs[/dim]")
    uvicorn.run(dashboard_app, host=host, port=port)
