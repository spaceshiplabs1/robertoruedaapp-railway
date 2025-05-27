#!/bin/bash
set -e

# Debug: Show environment variables
echo "🚀 Railway Deployment Starting..."
echo "📊 Database Host: ${DB_HOST:-NOT_SET}"
echo "📊 Database Name: ${DB_NAME:-NOT_SET}"
echo "📊 Database User: ${DB_USER:-NOT_SET}"
echo "🔧 Workers: ${WORKERS:-NOT_SET}"
echo "📁 Addons Path: ${ADDONS_PATH:-NOT_SET}"
echo "💾 Data Dir: ${DATA_DIR:-NOT_SET}"
echo "🔑 Enterprise Code: ${ENTERPRISE_CODE:-NOT_SET}"

# Create the final config file by substituting environment variables
echo "🔧 Creating Odoo configuration..."
envsubst < /etc/odoo/odoo.railway.conf > /etc/odoo/odoo.conf

# Check if database needs initialization
echo "🔍 Checking if database needs initialization..."
DB_INITIALIZED=$(PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='ir_module_module';" 2>/dev/null || echo "0")

if [ "$DB_INITIALIZED" = "0" ] || [ "$DB_INITIALIZED" = " 0" ]; then
    echo "🔧 Database not initialized, forcing initialization with base modules..."
    # Initialize database with base modules
    echo "🏗️ Running Odoo initialization..."
    /entrypoint.sh odoo -c /etc/odoo/odoo.conf -i base --stop-after-init --no-http
    echo "✅ Database initialization complete!"
fi

echo "🔧 ODOO_DATA_DIR set to handle filestore permissions automatically"

# Show the generated config for debugging
echo "📋 Generated configuration:"
cat /etc/odoo/odoo.conf | head -20

# Note: Custom fitness seeding script available at /mnt/extra-addons/aplicar_semillado_fitness.sh
echo "🏋️‍♂️ Fitness module with custom seeding data available"
echo "📁 Custom addons path: /mnt/extra-addons"

# Call the original Odoo entrypoint to handle permissions and startup
exec /entrypoint.sh "$@" 