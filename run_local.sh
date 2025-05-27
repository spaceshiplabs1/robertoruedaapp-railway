#!/bin/bash

# Roberto Rueda Fitness App - Local Development Runner
echo "🚀 Starting Roberto Rueda Fitness App locally..."

# Activate virtual environment first
echo "🔧 Activating virtual environment..."
source odoo-18.0+e.20250521/odoo-venv/bin/activate

# Load local environment variables
export $(cat local.env | grep -v ^# | xargs)

# Kill any existing Odoo processes
echo "🔄 Checking for existing Odoo processes..."
pkill -f "odoo" 2>/dev/null || true
pkill -f "python.*odoo" 2>/dev/null || true
sleep 2

# Ensure filestore directory exists
mkdir -p odoo-18.0+e.20250521/filestore

# Start Odoo with local configuration
echo "🎯 Starting Odoo locally on http://localhost:8069"
echo "📁 Using local database: test_odoo"
echo "🔧 Using addons from: custom_addons and odoo/addons"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================="

cd odoo-18.0+e.20250521

# Try to find odoo-bin first, if not available use direct Python
if [ -f "odoo-bin" ]; then
    echo "Using odoo-bin..."
    python3 odoo-bin \
        --config=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo.conf \
        --addons-path=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/custom_addons,/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/odoo/addons \
        --database=test_odoo \
        --db-filter=test_odoo \
        --without-demo=all \
        --data-dir=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/filestore \
        --dev=reload,qweb,werkzeug,xml \
        --log-level=info \
        --workers=0
else
    echo "Using Python direct execution..."
    PYTHONPATH=. python3 -c "
import sys
import os
sys.path.insert(0, '.')
os.chdir('.')

# Set up the command line arguments
import odoo
from odoo.tools import config

# Parse configuration
config.parse_config([
    '--config=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo.conf',
    '--addons-path=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/custom_addons,/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/odoo/addons',
    '--database=test_odoo',
    '--db-filter=test_odoo',
    '--without-demo=all',
    '--data-dir=/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521/filestore',
    '--dev=reload,qweb,werkzeug,xml',
    '--log-level=info',
    '--workers=0'
])

# Start the server
import odoo.service.server
odoo.service.server.start(preload=[], stop=False)
"
fi 