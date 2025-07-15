"""
CEENI Platform - Config Init

This file ensures the custom `apps/` directory is discoverable as a Python package
by injecting it into the Python path at runtime.

This allows Django to find modular apps like `accounts`, `profiles`, `projects`, etc.,
without needing `apps.` prefix in imports.

Inspired by Django best practices for scalable modular architecture.
"""

# ------------------------------------------------------------------------------
# PYTHON PATH CONFIGURATION
# ------------------------------------------------------------------------------

import sys
from pathlib import Path

# Append the `apps/` directory to Python path
# This allows importing apps directly like: from accounts.models import CustomUser
sys.path.append(str(Path(__file__).resolve().parent.parent / "apps"))
