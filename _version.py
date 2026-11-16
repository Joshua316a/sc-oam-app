"""sc-oam-app version information — Single source of truth.

All parts of the project should import version from this module
rather than defining it inline. This prevents the version drift
that OAMv1 experienced (version defined in 10+ places).
"""

__version__ = "0.1.0"

# Derived for convenience
VERSION = __version__
VERSION_MAJOR = int(__version__.split(".")[0])
VERSION_MINOR = int(__version__.split(".")[1])
PATCH = "0"  # Updated manually for hotfixes

# Human-readable form
version_string = __version__

# PEP 440 compatible
