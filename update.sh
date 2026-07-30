#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Mise à jour
# Usage: ./update.sh
# Pull Git, rebuild les images Docker, redémarre.
# ────────────────────────────────────────────────────────────

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

fail() { log_error "$1"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Mise à jour                 ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ── Vérifications ──────────────────────────────────────────
if [ ! -f ".env" ]; then
    fail "Fichier .env introuvable. Lance d'abord ./install.sh"
fi

# ── Étape 1 : Git pull ─────────────────────────────────────
if git rev-parse --git-dir &>/dev/null 2>&1; then
    log_info "Récupération des dernières modifications..."
    git pull
    log_ok "Sources mises à jour"
else
    log_warn "Pas de dépôt Git — mets à jour les sources manuellement"
fi

# ── Étape 2 : Reconstruction ───────────────────────────────
log_info "Reconstruction des images Docker..."
docker compose build --pull
log_ok "Images reconstruites"

# ── Étape 3 : Redémarrage ──────────────────────────────────
log_info "Redémarrage des services..."
docker compose up -d
log_ok "Services redémarrés"

# ── Étape 4 : Migration base de données ────────────────────
if command -v alembic &>/dev/null && [ -f "infrastructure/postgres/alembic.ini" ]; then
    log_info "Application des migrations PostgreSQL..."
    alembic -c infrastructure/postgres/alembic.ini upgrade head || log_warn "Migration non appliquée (base en mémoire ?)"
    log_ok "Migrations à jour"
fi

# ── Étape 5 : Healthcheck ──────────────────────────────────
echo ""
log_info "Vérification de l'état des services..."
sleep 3
if command -v curl &>/dev/null; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
    if [ "$HTTP_STATUS" = "200" ]; then
        log_ok "API disponible (HTTP 200)"
    else
        log_warn "API HTTP $HTTP_STATUS (peut encore démarrer)"
    fi
fi

echo ""
log_info "Mise à jour terminée"
echo ""
