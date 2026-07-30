#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Update
# Usage: ./update.sh
# Pull les dernières images, rebuild si nécessaire, redémarre.
# ────────────────────────────────────────────────────────────

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Mise à jour                 ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Ensure .env exists
if [ ! -f ".env" ]; then
    fail "Fichier .env introuvable. Lance d'abord ./install.sh"
fi

# Step 1: Pull latest
log_info "Recuperation des dernieres modifications..."
if git rev-parse --git-dir &>/dev/null 2>&1; then
    git pull
    log_ok "Sources mises à jour"
else
    log_warn "Pas de depot git — mets à jour les sources manuellement"
fi

# Step 2: Rebuild images
log_info "Reconstruction des images Docker..."
docker compose build --pull
log_ok "Images reconstruites"

# Step 3: Restart
log_info "Redemarrage des services..."
docker compose up -d
log_ok "Services redemarres"

# Step 4: Healthcheck
echo ""
log_info "Verification de l'etat des services..."
sleep 3
if command -v curl &>/dev/null; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [ "$HTTP_STATUS" = "200" ]; then
        log_ok "API disponible (HTTP 200)"
    else
        log_warn "API HTTP $HTTP_STATUS (peut encore demarrer)"
    fi
fi

log_info "Mise à jour terminee"
