#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Développement local (FastAPI + Vite)
# Usage: ./dev.sh
# Nécessite PYTHONPATH configuré (via source scripts/activate_env.sh).
# Lance le backend FastAPI avec --reload et le frontend Vite.
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
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_info "Fichier .env créé"
    else
        log_error ".env.example introuvable"
        exit 1
    fi
fi

if [ -z "${PYTHONPATH:-}" ]; then
    log_warn "PYTHONPATH non défini — activation de l'environnement"
    if [ -f "scripts/activate_env.sh" ]; then
        # shellcheck disable=SC1091
        source scripts/activate_env.sh
    else
        log_error "scripts/activate_env.sh introuvable"
        log_info "Configure PYTHONPATH manuellement :"
        log_info "  source scripts/activate_env.sh"
        log_info "  ou consulte le Makefile pour la variable PYTHONPATH"
        exit 1
    fi
fi

# ── Nettoyage à l'arrêt ────────────────────────────────────
cleanup() {
    log_info "Arrêt des services..."
    kill "$API_PID" 2>/dev/null || true
    kill "$FRONTEND_PID" 2>/dev/null || true
    wait "$API_PID" 2>/dev/null || true
    wait "$FRONTEND_PID" 2>/dev/null || true
    log_ok "Services arrêtés"
}
trap cleanup EXIT INT TERM

# ── Démarrage API ──────────────────────────────────────────
log_info "Démarrage du backend FastAPI..."
PYTHONPATH="$PYTHONPATH" python3 -m uvicorn callibr_api.main:create_app \
    --factory \
    --app-dir apps/api/src \
    --reload \
    --host 0.0.0.0 \
    --port 8000 &
API_PID=$!
log_ok "Backend démarré (PID $API_PID)"

# ── Attente API ────────────────────────────────────────────
log_info "Attente de l'API..."
for i in $(seq 1 15); do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q "200"; then
        log_ok "API disponible sur http://localhost:8000"
        break
    fi
    if [ "$i" -eq 15 ]; then
        log_warn "L'API n'a pas répondu — vérifie les logs"
    fi
    sleep 1
done

# ── Démarrage Frontend ─────────────────────────────────────
log_info "Démarrage du frontend Vite..."
cd apps/frontend
npm run dev &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"
log_ok "Frontend démarré (PID $FRONTEND_PID)"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Mode développement          ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Frontend : ${CYAN}http://localhost:5173${NC}"
echo -e "  API      : ${CYAN}http://localhost:8000${NC}"
echo -e "  Docs     : ${CYAN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  Appuie sur ${YELLOW}Ctrl+C${NC} pour arrêter les deux services"
echo ""

wait
