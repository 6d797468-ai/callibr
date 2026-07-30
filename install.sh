#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Installer
# Usage: ./install.sh
# Détecte l'OS, vérifie les dépendances, copie .env, lance make dev.
# ────────────────────────────────────────────────────────────

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

fail() {
    log_error "$1"
    exit 1
}

# ── Welcome ────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Installation                ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ── OS Detection ───────────────────────────────────────────
OS="$(uname -s)"
ARCH="$(uname -m)"
log_info "Systeme     : $OS $ARCH"

# ── Dependency checks ──────────────────────────────────────

check_cmd() {
    if ! command -v "$1" &>/dev/null; then
        fail "$1 n'est pas installe. $2"
    fi
    log_ok "$1 trouve"
}

check_cmd "docker"   "Installe Docker : https://docs.docker.com/get-docker/"
check_cmd "docker"   "Assure-toi que Docker est dans ton PATH"

# Docker Compose (standalone v2 or plugin)
if docker compose version &>/dev/null; then
    DOCKER_COMPOSE="docker compose"
    log_ok "docker compose (plugin)"
elif docker-compose --version &>/dev/null; then
    DOCKER_COMPOSE="docker-compose"
    log_ok "docker-compose (standalone)"
else
    fail "docker compose introuvable. Installe Docker Compose : https://docs.docker.com/compose/install/"
fi

# Optional: Python (for local dev without Docker)
if command -v python3 &>/dev/null; then
    PYTHON_OK=true
    log_ok "python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
else
    PYTHON_OK=false
    log_warn "python3 non trouve (uniquement necessaire pour le developpement local sans Docker)"
fi

# ── Docker readiness ───────────────────────────────────────
if ! docker info &>/dev/null; then
    fail "Docker n'est pas en cours d'execution. Lance Docker Desktop ou demarre le service Docker."
fi
log_ok "Docker est en cours d'execution"

# ── Project setup ──────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_info "Fichier .env cree depuis .env.example"
    log_warn "Renseigne les cles API dans .env avant de lancer l'application"
    log_warn "  Voir ROTATION-REPORT.md pour la liste des variables requises"
else
    log_ok ".env existe deja"
fi

# ── Summary ────────────────────────────────────────────────
echo ""
log_info "Installation terminee."
echo ""
echo -e "  ${CYAN}Pret a demarrer :${NC}"
echo -e "    1. Edite le fichier .env avec tes cles API"
echo -e "    2. Lance :  ${CYAN}docker compose up${NC}"
echo -e "    3. Verifie : ${CYAN}./healthcheck.sh${NC}"
echo ""
