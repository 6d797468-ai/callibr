#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Activation de l'environnement virtuel
# Usage: source scripts/activate_env.sh
# Crée le .venv si nécessaire, installe les dépendances
# et configure PYTHONPATH.
# ────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Détection du mode source (obligatoire)
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    log_error "Ce script doit être sourcé : source scripts/activate_env.sh"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

cd "$PROJECT_DIR"

# ── Création du venv ───────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    log_info "Création de l'environnement virtuel..."
    python3 -m venv "$VENV_DIR"
    log_ok "Environnement virtuel créé dans .venv"
fi

# ── Activation ─────────────────────────────────────────────
source "$VENV_DIR/bin/activate"
log_ok "Environnement virtuel activé : $(which python3)"

# ── Installation des dépendances ───────────────────────────
if [ -f "pyproject.toml" ]; then
    pip install --quiet -e . 2>/dev/null || \
        pip install --quiet -e ".[dev]" 2>/dev/null || \
        log_warn "pip install -e . a échoué — installation manuelle des dépendances nécessaire"
fi

# ── PYTHONPATH ─────────────────────────────────────────────
PYTHONPATH_APPEND=""
for pkg in \
    apps/api/src \
    packages/kernel/src \
    packages/contracts/src \
    packages/persistence/src \
    packages/shared/src \
    packages/telemetry/src \
    packages/seed/src \
    platform/identity/src \
    engines/crm/src \
    engines/conversation/src \
    engines/evaluation/src \
    engines/persona/src \
    engines/procedure/src \
    engines/rule/src \
    engines/scenario/src \
    engines/simulation/src \
    engines/planning/src \
    engines/director/src \
    engines/voice/src; do
    if [ -d "$PROJECT_DIR/$pkg" ]; then
        PYTHONPATH_APPEND="${PYTHONPATH_APPEND:+$PYTHONPATH_APPEND:}$PROJECT_DIR/$pkg"
    fi
done

export PYTHONPATH="${PYTHONPATH_APPEND:=$PYTHONPATH}"
log_ok "PYTHONPATH configuré"

echo ""
echo -e "${CYAN}Callibr — Environnement prêt${NC}"
echo -e "  Python : $(which python3)"
echo -e "  Lance le développement avec : ${CYAN}./dev.sh${NC}"
echo ""
