"""FastAPI application factory for the OpenEC REST API.

Exposes all registered commands as REST endpoints with auto-generated
OpenAPI/Swagger documentation.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from openec_platform.core.command_runner import CommandRunner
from openec_platform.core.oecject import OECject
from openec_platform.core.router import Router


def create_app(router: Router) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        router: The root router with all registered commands.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="OpenEC API",
        description=(
            "OpenEC - Open Source AI-Powered Ecommerce & Retail Analytics Platform. "
            "Unified API for product analytics, order tracking, customer insights, "
            "inventory management, marketing attribution, and pricing intelligence."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    runner = CommandRunner(router)

    @app.get("/")
    async def root() -> Dict[str, Any]:
        return {
            "name": "OpenEC API",
            "version": "0.1.0",
            "description": "Open Source AI-Powered Ecommerce & Retail Analytics",
            "docs": "/docs",
            "commands": runner.list_commands(),
        }

    @app.get("/api/v1/commands")
    async def list_commands() -> Dict[str, Any]:
        return {"commands": runner.list_commands()}

    # Auto-register all commands as GET endpoints
    commands = router.get_all_commands()
    for path, cmd in commands.items():
        api_path = f"/api/v1{path}"

        # Create a closure to capture cmd
        def _make_endpoint(command_info):
            async def endpoint(
                provider: str = Query("demo", description="Data provider to use"),
            ) -> Dict[str, Any]:
                try:
                    result = runner.run(command_info.path, provider=provider)
                    return result.model_dump(mode="json")
                except KeyError as e:
                    raise HTTPException(status_code=404, detail=str(e))
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))

            endpoint.__doc__ = command_info.description
            return endpoint

        app.add_api_route(
            api_path,
            _make_endpoint(cmd),
            methods=["GET"],
            tags=cmd.tags or [cmd.path.split("/")[1]] if "/" in cmd.path else ["general"],
            summary=cmd.description,
        )

    return app
