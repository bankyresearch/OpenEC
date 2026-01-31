"""Command runner - executes registered commands with provider resolution."""

from __future__ import annotations

from typing import Any, Dict, Optional

from openec_platform.core.oecject import OECject
from openec_platform.core.provider_interface import QueryParams, registry
from openec_platform.core.router import CommandInfo, Router


class CommandRunner:
    """Executes commands registered in the router, resolving providers automatically.

    The runner:
    1. Looks up the command by path
    2. Resolves the provider from the registry
    3. Calls the fetcher's fetch() then transform()
    4. Wraps the result in an OECject
    """

    def __init__(self, router: Router) -> None:
        self.router = router

    def run(self, path: str, provider: str = "demo", **kwargs: Any) -> OECject:
        """Execute a command by its path.

        Args:
            path: The command path (e.g., "/products/sales/historical").
            provider: The data provider to use.
            **kwargs: Parameters passed to the provider fetcher.

        Returns:
            OECject containing the results.
        """
        commands = self.router.get_all_commands()
        if path not in commands:
            available = "\n  ".join(sorted(commands.keys()))
            raise KeyError(f"Command '{path}' not found. Available:\n  {available}")

        cmd = commands[path]
        model_name = cmd.model

        if model_name and cmd.provider_choices:
            fetcher = registry.get_fetcher(provider, model_name)
            params = QueryParams(provider=provider, **kwargs)
            raw = fetcher.fetch(params, **kwargs)
            results = fetcher.transform(raw, **kwargs)
        else:
            # Direct function call (no provider needed)
            results = cmd.func(**kwargs)

        return OECject(
            results=results,
            provider=provider,
            model=model_name or "",
            command=path,
        )

    def list_commands(self) -> list[str]:
        """List all available command paths."""
        return self.router.list_routes()
