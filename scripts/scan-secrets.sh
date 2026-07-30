#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr Secret Scanner — Release Gate helper
# Detects potential credentials in tracked files
# ────────────────────────────────────────────────────────────
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Patterns known to indicate secrets (from common API key formats)
SECRET_PATTERNS=(
  'sk-proj-[A-Za-z0-9_-]{20,}'      # OpenAI project key
  'sk-or-v1-[A-Za-z0-9_-]{20,}'     # OpenRouter
  'AIzaSy[A-Za-z0-9_-]{30,}'        # Google API key
  'GOCSPX-[A-Za-z0-9_-]{20,}'       # Google OAuth secret
  'ghp_[A-Za-z0-9_-]{20,}'          # GitHub PAT
  'gho_[A-Za-z0-9_-]{20,}'          # GitHub OAuth
  'ghu_[A-Za-z0-9_-]{20,}'          # GitHub user token
  'xox[bpors]-[A-Za-z0-9_-]{20,}'  # Slack tokens
  'AKIA[A-Z0-9]{16}'                # AWS access key
)

SCAN_DIR="${1:-.}"
EXIT_CODE=0

# Files that are allowed to contain dummy/example secrets
ALLOWED_PATTERNS=(
  '\.env\.example$'
  'test_.*\.py$'
  'scan-secrets\.sh$'
)

should_skip() {
  local file="$1"
  for pat in "${ALLOWED_PATTERNS[@]}"; do
    if echo "$file" | grep -qE "$pat"; then
      return 0
    fi
  done
  return 1
}

echo "🔍 Scanning for secrets in $SCAN_DIR ..."
echo ""

while IFS= read -r -d '' file; do
  # Skip binary files
  if file "$file" | grep -q "binary"; then
    continue
  fi

  if should_skip "$file"; then
    continue
  fi

  for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -qnE "$pattern" "$file" 2>/dev/null; then
      echo -e "${RED}⚠️  Potential secret found in: $file${NC}"
      grep -nE "$pattern" "$file" | head -3
      echo ""
      EXIT_CODE=1
    fi
  done
done < <(find "$SCAN_DIR" -type f -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/venv/*' -not -path '*/__pycache__/*' -print0)

if [ "$EXIT_CODE" -eq 0 ]; then
  echo -e "${GREEN}✅ No secrets detected.${NC}"
fi

exit "$EXIT_CODE"
