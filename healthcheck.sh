#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────
# Callibr — Healthcheck
# Usage: ./healthcheck.sh
# Vérifie que tous les services Callibr répondent.
# Retourne 0 si tout va bien, 1 sinon.
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

FAILED=0

check_http() {
    local name="$1"
    local url="$2"
    local expected="${3:-200}"
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    if [ "$status" = "$expected" ]; then
        log_ok "$name ($url → $status)"
    else
        log_error "$name ($url → $status, attendu $expected)"
        FAILED=1
    fi
}

check_docker() {
    local service="$1"
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "$service"; then
        log_ok "Conteneur '$service' en cours d'exécution"
    else
        local status
        status=$(docker ps -a --format '{{.Names}} {{.State}}' 2>/dev/null | grep "$service" || true)
        if [ -n "$status" ]; then
            log_warn "Conteneur '$service' existe mais : $status"
        else
            log_error "Conteneur '$service' introuvable"
        fi
        FAILED=1
    fi
}

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         Callibr — Healthcheck                 ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# ── Docker ─────────────────────────────────────────────────
if docker info &>/dev/null; then
    log_info "Conteneurs Docker :"
    check_docker "callibr-api"
    check_docker "callibr-frontend"
    check_docker "postgres"
    check_docker "redis"
else
    log_warn "Docker non disponible — vérification réduite"
fi

echo ""

# ── API HTTP ───────────────────────────────────────────────
log_info "Points d'accès HTTP :"
check_http "Health endpoint" "http://localhost:8000/health" 200
check_http "Platform info" "http://localhost:8000/api/v1/platform/info" 200
check_http "Documentation OpenAPI" "http://localhost:8000/openapi.json" 200
check_http "Metrics Prometheus" "http://localhost:8000/metrics" 200

echo ""

# ── Frontend ───────────────────────────────────────────────
check_http "Frontend" "http://localhost:5173" 200

echo ""

# ── Résultat ───────────────────────────────────────────────
if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}Tous les services Callibr sont opérationnels.${NC}"
    exit 0
else
    echo -e "${RED}Des services Callibr rencontrent des problèmes.${NC}"
    echo ""
    echo "Diagnostic :"
    echo "  docker ps -a"
    echo "  docker compose logs api"
    echo "  docker compose logs frontend"
    exit 1
fi
