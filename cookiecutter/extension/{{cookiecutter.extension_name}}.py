"""{{cookiecutter.extension_name}} extension for OpenEC."""

from openec_platform.core.router import Router

router = Router(prefix="/{{cookiecutter.extension_name}}")


@router.command(model="{{cookiecutter.model_name}}", description="{{cookiecutter.description}}")
def {{cookiecutter.command_name}}(provider: str = "demo"):
    """{{cookiecutter.description}}"""
    pass
