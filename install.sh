#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Installation
# Usage: ./install.sh
# Vérifie les prérequis, copie .env, construit les images.
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

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Installation                ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ── OS ─────────────────────────────────────────────────────
log_info "Système : $(uname -s) $(uname -m)"

# ── Dépendances ────────────────────────────────────────────
check_cmd() {
    if ! command -v "$1" &>/dev/null; then
        fail "$1 n'est pas installé. $2"
    fi
    log_ok "$1 trouvé"
}

check_cmd "docker" "Installe Docker : https://docs.docker.com/get-docker/"

if docker compose version &>/dev/null; then
    DOCKER_COMPOSE="docker compose"
    log_ok "docker compose (plugin)"
elif docker-compose --version &>/dev/null; then
    DOCKER_COMPOSE="docker-compose"
    log_ok "docker-compose (standalone)"
else
    fail "docker compose introuvable. Installe Docker Compose."
fi

if ! docker info &>/dev/null; then
    fail "Docker n'est pas en cours d'exécution"
fi
log_ok "Docker est en cours d'exécution"

# ── Projet ─────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_info "Fichier .env créé depuis .env.example"
        log_warn "Édite .env pour renseigner les clés API nécessaires"
    else
        fail ".env.example introuvable"
    fi
else
    log_ok ".env existe déjà"
fi

# ── Build ──────────────────────────────────────────────────
log_info "Construction des images Docker..."
$DOCKER_COMPOSE build
log_ok "Images construites"

# ── Résumé ─────────────────────────────────────────────────
echo ""
log_info "Installation terminée."
echo ""
echo -e "  ${CYAN}Pour démarrer :${NC}"
echo -e "    ${CYAN}./start.sh${NC}"
echo ""
echo -e "  ${CYAN}Pour vérifier :${NC}"
echo -e "    ${CYAN}./healthcheck.sh${NC}"
echo ""
