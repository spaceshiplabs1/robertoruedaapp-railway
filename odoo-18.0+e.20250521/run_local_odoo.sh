#!/bin/bash

# Kill any existing Odoo instances
echo "🔍 Checking for existing Odoo instances..."
ODOO_PIDS=$(ps aux | grep '[p]ython.*odoo' | grep -v grep | awk '{print $2}')

if [ ! -z "$ODOO_PIDS" ]; then
    echo "💀 Killing existing Odoo processes: $ODOO_PIDS"
    echo "$ODOO_PIDS" | xargs kill -9
    sleep 2
    echo "✅ Existing Odoo instances terminated"
else
    echo "✅ No existing Odoo instances found"
fi

# Kill any processes using port 8069
echo "🔍 Checking port 8069..."
PORT_PID=$(lsof -ti:8069)
if [ ! -z "$PORT_PID" ]; then
    echo "💀 Killing process using port 8069: $PORT_PID"
    kill -9 $PORT_PID
    sleep 1
    echo "✅ Port 8069 freed"
else
    echo "✅ Port 8069 is available"
fi

# Load local environment variables
export $(cat ../local.env | grep -v '^#' | xargs)

echo ""
echo "🚀 Starting Odoo locally with odoo_test database..."
echo "📊 Configuration:"
echo "   Database: $DB_NAME@$DB_HOST"
echo "   Port: $PORT"
echo "   Addons: $ADDONS_PATH"
echo ""

# Start Odoo with loaded environment
python -m odoo \
    --config=../odoo.conf \
    --addons-path="$ADDONS_PATH" \
    --database="$DB_NAME" \
    --dev=reload,qweb,werkzeug,xml 