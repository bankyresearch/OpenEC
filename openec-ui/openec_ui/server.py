"""FastAPI server that serves the React dashboard and mounts the OpenEC API."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    """Create the combined dashboard + API application."""
    from openec_cli.main import _get_runner
    from openec_platform.core.api import create_app as create_api_app

    runner, root = _get_runner()
    api_app = create_api_app(root)

    app = FastAPI(
        title="OpenEC Dashboard",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount the openec API
    app.mount("/api", api_app)

    # Serve static assets (JS, CSS)
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    # SPA fallback: serve index.html for all non-API routes
    index_html = STATIC_DIR / "index.html"

    @app.get("/docs")
    async def docs_redirect():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/docs")

    @app.get("/{path:path}")
    async def serve_spa(request: Request, path: str):
        # Check if it's a static file first
        static_file = STATIC_DIR / path
        if path and static_file.exists() and static_file.is_file():
            return FileResponse(str(static_file))
        # Otherwise serve index.html for client-side routing
        return FileResponse(str(index_html))

    return app
