"""attachments: A modern Python library.

This package is structured with a src/ layout and configured
to use uv for environment and dependency management and ruff
for linting and formatting.
"""

from .tst import tst as testy

__all__: list[str] = ["testy"]

# Managed via [tool.hatch.version] in pyproject.toml
__version__ = "0.1.0"
