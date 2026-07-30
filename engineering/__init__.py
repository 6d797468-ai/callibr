"""
Callibr Engineering Automation System

Usage:
    python -m engineering doctor
    python -m engineering verify
    python -m engineering repair
    python -m engineering check <check_name>
"""

import sys

from engineering.cli import main

if __name__ == "__main__":
    sys.exit(main())
