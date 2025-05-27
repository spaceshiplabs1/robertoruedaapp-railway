#!/bin/bash

# Script para reiniciar Odoo - Proyecto Fitness
echo "🏋️‍♂️ Reiniciando Odoo - Proyecto Fitness"
echo "========================================"

# Configuración
ODOO_ROOT="/Users/spaceshiplabs/Documents/robertoruedaapp/odoo-18.0+e.20250521"
ODOO_VENV="$ODOO_ROOT/odoo-venv"
DB_NAME="odoo_test"

# Función para matar procesos de Odoo
kill_odoo() {
    echo "🔍 Buscando procesos de Odoo..."
    
    # Buscar procesos de Python que contengan 'odoo'
    ODOO_PIDS=$(ps aux | grep -E "python.*odoo" | grep -v grep | awk '{print $2}')
    
    if [ -z "$ODOO_PIDS" ]; then
        echo "✅ No se encontraron procesos de Odoo ejecutándose"
    else
        echo "🔪 Matando procesos de Odoo: $ODOO_PIDS"
        echo "$ODOO_PIDS" | xargs kill -9 2>/dev/null
        sleep 2
        echo "✅ Procesos de Odoo terminados"
    fi
}

# Función para matar procesos en puertos específicos
kill_ports() {
    echo "🔍 Verificando puertos 8069 y 8071..."
    
    # Puerto 8069 (Odoo web)
    PORT_8069=$(lsof -ti:8069)
    if [ ! -z "$PORT_8069" ]; then
        echo "🔪 Matando proceso en puerto 8069: $PORT_8069"
        kill -9 $PORT_8069 2>/dev/null
    fi
    
    # Puerto 8071 (Odoo longpolling)
    PORT_8071=$(lsof -ti:8071)
    if [ ! -z "$PORT_8071" ]; then
        echo "🔪 Matando proceso en puerto 8071: $PORT_8071"
        kill -9 $PORT_8071 2>/dev/null
    fi
    
    echo "✅ Puertos liberados"
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
    
    # Iniciar Odoo
    python -m odoo --addons-path=odoo/addons,custom_addons -d "$DB_NAME"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  kill     - Solo matar procesos de Odoo"
    echo "  start    - Solo iniciar Odoo"
    echo "  restart  - Matar procesos e iniciar (por defecto)"
    echo "  help     - Mostrar esta ayuda"
    echo ""
}

# Función principal
main() {
    case "${1:-restart}" in
        "kill")
            kill_odoo
            kill_ports
            echo "🏁 Procesos de Odoo terminados"
            ;;
        "start")
            start_odoo
            ;;
        "restart")
            kill_odoo
            kill_ports
            echo "⏳ Esperando 3 segundos..."
            sleep 3
            start_odoo
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo "❌ Opción no válida: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal con argumentos
main "$@" 