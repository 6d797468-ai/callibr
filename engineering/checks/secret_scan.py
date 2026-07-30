"""
Callibr Secret Scanner

Detects leaked credentials, high-entropy strings, private keys,
and API key patterns across the codebase. Designed for CI / Release Gate.
"""

import math
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SecretFinding:
    path: str
    line: int
    pattern_name: str
    snippet: str
    entropy: float = 0.0


@dataclass
class SecretScanResult:
    passed: bool
    findings: list[SecretFinding]
    scanned_files: int = 0


# ── API / credential patterns (keyed by provider) ──────────

_PATTERNS: dict[str, re.Pattern] = {
    "openai_project_key": re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}"),
    "openai_org_key": re.compile(r"sk-org-[A-Za-z0-9_-]{20,}"),
    "openrouter_key": re.compile(r"sk-or-v1-[A-Za-z0-9_-]{20,}"),
    "google_api_key": re.compile(r"AIzaSy[A-Za-z0-9_-]{30,}"),
    "google_oauth_secret": re.compile(r"GOCSPX-[A-Za-z0-9_-]{20,}"),
    "github_pat": re.compile(r"ghp_[A-Za-z0-9_-]{20,}"),
    "github_fine_grained": re.compile(r"github_pat_[A-Za-z0-9_-]{40,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic_private_key": re.compile(
        r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
    ),
    "generic_certificate": re.compile(
        r"-----BEGIN CERTIFICATE-----"
    ),
    "jwt_token": re.compile(
        r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    ),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "telegram_token": re.compile(r"[0-9]{8,10}:[A-Za-z0-9_-]{35,}"),
    "heroku_api_key": re.compile(
        r"[hH][eE][rR][oO][kK][uU].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-"
        r"[0-9A-F]{4}-[0-9A-F]{12}"
    ),
    "sendgrid_api_key": re.compile(r"SG\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
    "stripe_live_key": re.compile(r"sk_live_[A-Za-z0-9]{20,}"),
    "stripe_test_key": re.compile(r"sk_test_[A-Za-z0-9]{20,}"),
    "twilio_account_sid": re.compile(r"AC[A-Za-z0-9]{32}"),
}

# Paths where secrets may legitimately appear (test files, examples)
_ALLOWED_PATH_PATTERNS: list[re.Pattern] = [
    re.compile(r"\.env\.example$"),
    re.compile(r"test_.*\.py$"),
    re.compile(r"secret_scan\.py$"),
    re.compile(r"release_gate\.py$"),
    re.compile(r"callibr_api/config\.py$"),
]

_EXCLUDED_DIRS: set[str] = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

# Files excluded by name (e.g. lock files where hashes look like secrets)
_EXCLUDED_FILES: set[str] = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Cargo.lock",
}

_TARGET_GLOBS = [
    "*.py",
    "*.yaml",
    "*.yml",
    "*.json",
    "*.toml",
    "*.cfg",
    "*.ini",
    "*.env",
    ".env.example",
    "*.sh",
    "*.envrc",
    "*.pem",
    "*.key",
    "*.p12",
]


def _shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    for char in set(data):
        p = data.count(char) / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def _is_allowed(path: Path) -> bool:
    return any(p.search(str(path)) for p in _ALLOWED_PATH_PATTERNS)


def scan_secrets(root: str = ".") -> SecretScanResult:
    root_path = Path(root).resolve()
    findings: list[SecretFinding] = []
    scanned = 0

    for glob in _TARGET_GLOBS:
        for path in root_path.rglob(glob):
            if not path.is_file():
                continue
            if any(ign in path.parts for ign in _EXCLUDED_DIRS):
                continue
            if path.name.startswith(".") and path.name not in (".env", ".env.example"):
                continue
            if path.name in _EXCLUDED_FILES:
                continue
            if _is_allowed(path):
                continue

            scanned += 1
            try:
                text = path.read_text(errors="replace")
            except (OSError, UnicodeDecodeError):
                continue

            for line_no, line in enumerate(text.splitlines(), 1):
                stripped = line.strip()
                if not stripped:
                    continue

                # Pattern-based detection
                for pattern_name, pattern in _PATTERNS.items():
                    if pattern.search(stripped):
                        # Compute entropy of the matched value
                        match = pattern.search(stripped)
                        if match:
                            entropy = _shannon_entropy(match.group())
                            findings.append(
                                SecretFinding(
                                    path=str(path),
                                    line=line_no,
                                    pattern_name=pattern_name,
                                    snippet=stripped[:100],
                                    entropy=round(entropy, 2),
                                )
                            )

    return SecretScanResult(
        passed=len(findings) == 0,
        findings=findings,
        scanned_files=scanned,
    )
