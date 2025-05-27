#!/bin/bash

# Roberto Rueda Fitness App - Development Environment
echo "🐍 Activating Python 3.12 virtual environment..."

# Activate the correct Python environment
source odoo-18.0+e.20250521/odoo-venv/bin/activate

echo "✅ Python version: $(python --version)"
echo "🚀 Starting Odoo locally..."

# Change to Odoo directory and run
cd odoo-18.0+e.20250521
./run_local_odoo.sh 