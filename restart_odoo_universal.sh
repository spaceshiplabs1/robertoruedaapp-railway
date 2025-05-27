#!/bin/bash

# Script universal para reiniciar Odoo - Funciona desde cualquier ubicación
echo "🏋️‍♂️ Reiniciando Odoo - Proyecto Fitness (Universal)"
echo "===================================================="

# Configuración absoluta
ODOO_ROOT="/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521"
ODOO_VENV="$ODOO_ROOT/odoo-venv"
DB_NAME="odoo_test"

# Función para matar procesos de Odoo
kill_odoo_processes() {
    echo "🔍 Buscando procesos de Odoo..."
    
    # Matar procesos de Python que contengan 'odoo'
    pkill -f "python.*odoo" 2>/dev/null
    
    # Matar procesos en puertos específicos
    lsof -ti:8069 | xargs kill -9 2>/dev/null
    lsof -ti:8071 | xargs kill -9 2>/dev/null
    
    echo "✅ Procesos de Odoo terminados"
}

# Función para iniciar Odoo
start_odoo() {
    echo "🚀 Iniciando Odoo..."
    cd "$ODOO_ROOT"
    source "$ODOO_VENV/bin/activate"
    
    echo "📁 Directorio actual: $(pwd)"
    echo "🐍 Python: $(which python)"
    echo "🗄️  Base de datos: $DB_NAME"
    echo ""
    
    # Iniciar Odoo usando el archivo de configuración LOCAL
    python -m odoo -c /Users/spaceshiplabs/Documents/robertoruedaapp/odoo_local_dev.conf
}

# Función principal
main() {
    case "${1:-restart}" in
        "kill")
            kill_odoo_processes
            echo "🏁 Procesos de Odoo terminados"
            ;;
        "start")
            start_odoo
            ;;
        "restart"|"")
            kill_odoo_processes
            echo "⏳ Esperando 2 segundos..."
            sleep 2
            start_odoo
            ;;
        "help"|"-h"|"--help")
            echo "Uso: $0 [opción]"
            echo "Opciones:"
            echo "  kill     - Solo matar procesos de Odoo"
            echo "  start    - Solo iniciar Odoo"
            echo "  restart  - Matar procesos e iniciar (por defecto)"
            echo "  help     - Mostrar esta ayuda"
            ;;
        *)
            echo "❌ Opción no válida: $1"
            echo "Usa: $0 help para ver las opciones"
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@" 