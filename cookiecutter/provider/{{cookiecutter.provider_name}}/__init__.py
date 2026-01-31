"""{{cookiecutter.provider_name}} provider for OpenEC."""

from openec_platform.core.provider_interface import ProviderInfo

provider = ProviderInfo(
    name="{{cookiecutter.provider_name}}",
    description="{{cookiecutter.description}}",
    website="{{cookiecutter.website}}",
    credentials={{cookiecutter.credentials}},
)
