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

# Fix permissions for persistent volume (Railway mounts as root)
echo "🔧 Fixing filestore permissions..."
# Create directories with proper permissions if they don't exist
mkdir -p /app/filestore/sessions /app/filestore/filestore
chown -R odoo:odoo /app/filestore
chmod -R 755 /app/filestore

# Show the generated config for debugging
echo "📋 Generated configuration:"
cat /etc/odoo/odoo.conf | head -20

# Note: Custom fitness seeding script available at /mnt/extra-addons/aplicar_semillado_fitness.sh
echo "🏋️‍♂️ Fitness module with custom seeding data available"
echo "📁 Custom addons path: /mnt/extra-addons"

# Execute the original command
exec "$@" 