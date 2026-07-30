"""callibr_seed — Reference data bootstrapper.

Loads the shared demo catalogue (personas, procedures, rules, scenarios)
into the in-memory stores at application startup.  All definitions use the
public service interfaces so that the same code works regardless of the
persistence backend.
"""

from callibr_seed.loader import load_demo_catalogue

__all__ = ["load_demo_catalogue"]
