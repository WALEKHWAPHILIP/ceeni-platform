# ────────────────────────────────────────────────────────────────────────────────
# CEENI PLATFORM – Settings Loader
# This file acts as the switchboard for environment-specific Django settings.
# It decides whether to load `dev.py` or `prod.py` based on the DJANGO_ENV variable.
# ────────────────────────────────────────────────────────────────────────────────

import os  # Built-in Python module to access environment variables

# Load the current environment (default to 'dev' if not explicitly set)
env = os.getenv("DJANGO_ENV", "dev")

# Conditional import based on environment setting
if env == "prod":
    # In production mode, load the secure, locked-down settings
    from .prod import *
else:
    # In all other cases (including default), load development settings
    from .dev import *

