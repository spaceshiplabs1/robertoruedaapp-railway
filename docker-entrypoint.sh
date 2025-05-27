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

# Note: ODOO_DATA_DIR=/app/filestore is set, so Odoo will handle permissions
echo "🔧 ODOO_DATA_DIR set to handle filestore permissions automatically"

# Show the generated config for debugging
echo "📋 Generated configuration:"
cat /etc/odoo/odoo.conf | head -20

# Note: Custom fitness seeding script available at /mnt/extra-addons/aplicar_semillado_fitness.sh
echo "🏋️‍♂️ Fitness module with custom seeding data available"
echo "📁 Custom addons path: /mnt/extra-addons"

# Call the original Odoo entrypoint to handle permissions and startup
exec /entrypoint.sh "$@" 