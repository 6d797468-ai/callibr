#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Arrêt des services
# Usage: ./stop.sh
# Arrête les conteneurs Docker et libère les ressources.
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Arrêt                        ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ── Arrêt Docker ───────────────────────────────────────────
if docker compose version &>/dev/null 2>&1; then
    log_info "Arrêt des conteneurs Docker..."
    docker compose down
    log_ok "Conteneurs arrêtés"
elif docker-compose --version &>/dev/null 2>&1; then
    log_info "Arrêt des conteneurs Docker (standalone)..."
    docker-compose down
    log_ok "Conteneurs arrêtés"
else
    log_warn "docker compose non trouvé — recherche de conteneurs manuels..."
    # Vérifier les processus locaux
    for pid_file in /tmp/callibr-*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if kill "$pid" 2>/dev/null; then
                log_ok "Processus $pid arrêté"
            fi
            rm -f "$pid_file"
        fi
    done
fi

echo ""
log_ok "Callibr arrêté"
echo ""
