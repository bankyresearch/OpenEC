"""Command router with decorator-based registration, inspired by OpenBB's router pattern."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import BaseModel


@dataclass
class CommandInfo:
    """Metadata for a registered command."""

    path: str
    func: Callable
    model: Optional[str] = None
    description: str = ""
    provider_choices: bool = False
    tags: List[str] = field(default_factory=list)


class Router:
    """Hierarchical command router with decorator-based command registration.

    Usage:
        router = Router(prefix="/products")

        @router.command(model="SalesHistorical")
        def historical(symbol: str, provider: str = "demo") -> OECject:
            ...

    Routers can be nested via `include_router` to build the full command tree.
    """

    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix.rstrip("/")
        self._commands: Dict[str, CommandInfo] = {}
        self._sub_routers: List[Router] = []

    def command(
        self,
        model: Optional[str] = None,
        description: str = "",
        provider_choices: bool = True,
        tags: Optional[List[str]] = None,
    ) -> Callable:
        """Decorator to register a function as a platform command.

        Args:
            model: The standard model name this command returns.
            description: Human-readable description.
            provider_choices: Whether the command accepts a `provider` parameter.
            tags: Optional tags for grouping/filtering.
        """

        def decorator(func: Callable) -> Callable:
            path = f"{self.prefix}/{func.__name__}"
            cmd = CommandInfo(
                path=path,
                func=func,
                model=model,
                description=description or (func.__doc__ or "").strip().split("\n")[0],
                provider_choices=provider_choices,
                tags=tags or [],
            )
            self._commands[path] = cmd
            return func

        return decorator

    def include_router(self, router: "Router") -> None:
        """Mount a sub-router under this router's prefix."""
        router.prefix = f"{self.prefix}{router.prefix}"
        self._sub_routers.append(router)

    def get_all_commands(self) -> Dict[str, CommandInfo]:
        """Return all commands from this router and all sub-routers."""
        commands = dict(self._commands)
        for sub in self._sub_routers:
            commands.update(sub.get_all_commands())
        return commands

    def list_routes(self) -> List[str]:
        """Return sorted list of all registered command paths."""
        return sorted(self.get_all_commands().keys())
