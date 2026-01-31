"""OpenEC - Open Source AI-Powered Ecommerce & Retail Analytics Platform.

Usage:
    import openec

    # Access version
    openec.__version__

    # Quick access to core components
    from openec import Router, CommandRunner, OECject, ProviderRegistry
"""

from openec_platform import __version__
from openec_platform.core.command_runner import CommandRunner
from openec_platform.core.oecject import OECject
from openec_platform.core.provider_interface import (
    ProviderFetcher,
    ProviderInfo,
    ProviderRegistry,
    QueryParams,
    StandardModel,
    registry,
)
from openec_platform.core.router import Router

__all__ = [
    "__version__",
    "CommandRunner",
    "OECject",
    "ProviderFetcher",
    "ProviderInfo",
    "ProviderRegistry",
    "QueryParams",
    "Router",
    "StandardModel",
    "registry",
]
