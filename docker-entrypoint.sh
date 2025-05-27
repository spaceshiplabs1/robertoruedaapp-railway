#!/bin/bash
set -e

# Create the final config file by substituting environment variables
envsubst < /etc/odoo/odoo.railway.conf > /etc/odoo/odoo.conf

# Debug: Show the database connection being used
echo "🚀 Railway Deployment Starting..."
echo "📊 Database Host: $DB_HOST"
echo "📊 Database Name: $DB_NAME"
echo "📊 Database User: $DB_USER"
echo "🔧 Workers: $WORKERS"
echo "📁 Addons Path: $ADDONS_PATH"
echo "💾 Data Dir: $DATA_DIR"

# Execute the original command
exec "$@" 