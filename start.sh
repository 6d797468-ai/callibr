#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Démarrage complet (Docker)
# Usage: ./start.sh
# Construit, lance et attend la disponibilité des services.
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Vérifications ──────────────────────────────────────────
if [ ! -f ".env" ]; then
    log_warn "Fichier .env introuvable — création depuis .env.example"
    if [ ! -f ".env.example" ]; then
        log_error ".env.example introuvable"
        exit 1
    fi
    cp .env.example .env
    log_info "Fichier .env créé. Renseigne les clés API avant de démarrer."
fi

if ! docker info &>/dev/null; then
    log_error "Docker n'est pas en cours d'exécution"
    exit 1
fi

# ── Build ──────────────────────────────────────────────────
log_info "Construction des images Docker..."
docker compose build
log_ok "Images construites"

# ── Démarrage ──────────────────────────────────────────────
log_info "Démarrage des services..."
docker compose up -d
log_ok "Services lancés"

# ── Attente disponibilité ──────────────────────────────────
log_info "Attente de la disponibilité de l'API..."
for i in $(seq 1 30); do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q "200"; then
        log_ok "API disponible sur http://localhost:8000"
        break
    fi
    if [ "$i" -eq 30 ]; then
        log_error "L'API n'a pas démarré dans les délais"
        log_info "Consulte les logs : docker compose logs api"
        exit 1
    fi
    sleep 2
done

log_info "Attente du frontend..."
for i in $(seq 1 15); do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null | grep -q "200\|304"; then
        log_ok "Frontend disponible sur http://localhost:5173"
        break
    fi
    if [ "$i" -eq 15 ]; then
        log_warn "Le frontend n'a pas répondu (peut être en cours de compilation)"
    fi
    sleep 2
done

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Callibr est opérationnel              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Frontend : ${CYAN}http://localhost:5173${NC}"
echo -e "  API      : ${CYAN}http://localhost:8000${NC}"
echo -e "  Documentation : ${CYAN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  Pour arrêter : ${YELLOW}./stop.sh${NC}"
echo -e "  Pour vérifier : ${YELLOW}./healthcheck.sh${NC}"
echo ""
