#!/bin/bash

# Script rápido para reiniciar Odoo
echo "🔄 Reinicio rápido de Odoo..."

# Matar procesos de Odoo
pkill -f "python.*odoo" 2>/dev/null

# Matar procesos en puertos específicos
lsof -ti:8069 | xargs kill -9 2>/dev/null
lsof -ti:8071 | xargs kill -9 2>/dev/null

echo "✅ Procesos terminados"
echo "⏳ Esperando 2 segundos..."
sleep 2

# Ir a la carpeta correcta y activar entorno
cd "/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521"
source "odoo-venv/bin/activate"

echo "🚀 Iniciando Odoo..."
python -m odoo --addons-path=odoo/addons,custom_addons -d odoo_test 