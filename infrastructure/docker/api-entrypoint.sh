#!/usr/bin/env bash
set -e

# Extract DB host and port from URL or use defaults
DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}

echo "======================================"
echo "    Callibr API - Initialisation      "
echo "======================================"

echo "[1/3] En attente de la base de données PostgreSQL sur $DB_HOST:$DB_PORT..."
# Attendre que postgres soit disponible (netcat n'est pas forcément sur alpine/slim, 
# mais python l'est. Utilisons un mini script python pour vérifier le port)
python3 -c "
import socket, time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('$DB_HOST', int('$DB_PORT')))
        s.close()
        break
    except Exception:
        time.sleep(1)
"
echo "[OK] PostgreSQL est prêt."

echo "[2/3] Exécution des migrations Alembic (et Seed)..."
# Exécution depuis la racine du projet (là où PYTHONPATH inclut les sources)
export PYTHONPATH=/app/apps/api/src:/app/packages/kernel/src:/app/packages/contracts/src:/app/packages/persistence/src:/app/packages/shared/src:/app/packages/telemetry/src:/app/packages/seed/src:/app/platform/identity/src:/app/engines/crm/src:/app/engines/conversation/src:/app/engines/evaluation/src:/app/engines/persona/src:/app/engines/procedure/src:/app/engines/rule/src:/app/engines/scenario/src:/app/engines/simulation/src

python3 -m alembic -c infrastructure/postgres/alembic.ini upgrade head
echo "[OK] Migrations Alembic terminées."

echo "[3/3] Démarrage du processus principal..."
exec "$@"
