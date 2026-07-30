"""
Callibr Engineering Types
"""

from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    details: str = ""
