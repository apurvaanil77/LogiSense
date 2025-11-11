#!/bin/bash
set -e

########################################
# Detect OS
########################################
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    PY="python"                    # Windows Git Bash
    ACTIVATE="venv/Scripts/activate"
else
    PY="python3.11"                # macOS / Linux
    ACTIVATE="venv/bin/activate"
fi

########################################
# Create / Activate venv
########################################
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PY -m venv venv
fi

echo "🔄 Activating virtual environment..."
source "$ACTIVATE"

export PYTHONPATH=$(pwd)

###############################################
# INSTALL REQUIREMENTS FOR ALL SERVICES
###############################################
echo "📥 Installing dependencies for all services..."

REQS=(
    "services/ingestion_api/requirements.txt"
    "services/worker/requirements.txt"
    "services/analytics_api/requirements.txt"
    "services/dashboard/requirements.txt"
)

for req in "${REQS[@]}"; do
    if [ -f "$req" ]; then
        echo "📦 Installing → $req"
        pip install -r "$req"
    else
        echo "⚠️ Requirements not found: $req"
    fi
done

echo "✅ All requirements installed."

########################################
# Track PIDs
########################################
PIDS=()

########################################
# Run Flask service
########################################
run_service() {
    local MODULE=$1
    local PORT=$2
    local NAME=$3

    echo "🚀 Starting $NAME on port $PORT..."

    FLASK_APP="$MODULE" \
    FLASK_ENV=development \
    FLASK_DEBUG=1 \
    flask run --host=0.0.0.0 --port="$PORT" &

    PIDS+=($!)
}

########################################
# Cleanup on exit
########################################
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."

    for pid in "${PIDS[@]}"; do
        echo "⚡ Killing PID $pid"
        kill -9 "$pid" 2>/dev/null || true
    done

    echo "🧹 Cleaning orphan Flask/Celery processes on ports..."
    kill -9 $(lsof -t -i:8000) 2>/dev/null || true
    kill -9 $(lsof -t -i:5555) 2>/dev/null || true

    echo "✅ All services stopped. Ports released."
    exit 0
}

trap cleanup SIGINT

########################################
# Start services
########################################

echo "📌 Starting services..."
echo ""

# INGESTION API
run_service "services.ingestion_api.app" 8000 "Ingestion API"
echo "• Ingestion API → http://localhost:8000"

# WORKER (Python worker)
echo "🚀 Starting Python worker..."
$PY services/worker/app.py &
PIDS+=($!)

# FLOWER
echo "🚀 Starting Celery Flower → 5555..."
celery -A services.worker.app flower --port=5555 &
PIDS+=($!)

#ANALYTICS API
run_service "services.analytics_api.app" 8001 "Analytics API"
echo "• Analytics Api → http://localhost:8001"
# run_service "services.dashboard.app" 8003 "Dashboard API"

echo ""
echo "✅ All services running in DEV mode with auto-reload!"
echo "👉 Press CTRL+C to stop everything cleanly"

wait


# sudo lsof -i :8000
# kill -9 65624