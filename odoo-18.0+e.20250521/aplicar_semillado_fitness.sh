#!/bin/bash

echo "🏋️‍♂️ Aplicando Semillado del Módulo Fitness"
echo "=============================================="

# Verificar que Odoo esté ejecutándose
if ! pgrep -f "odoo" > /dev/null; then
    echo "❌ Odoo no está ejecutándose. Iniciando Odoo..."
    ./restart_odoo_universal.sh start &
    echo "⏳ Esperando 30 segundos para que Odoo inicie..."
    sleep 30
fi

echo "📦 Actualizando módulo mi_modulo_fitness..."

# Actualizar el módulo para cargar los nuevos datos
python -m odoo --addons-path=odoo/addons,custom_addons -d odoo_test -u mi_modulo_fitness --stop-after-init

if [ $? -eq 0 ]; then
    echo "✅ Semillado aplicado exitosamente!"
    echo ""
    echo "📊 Datos cargados:"
    echo "   FASE 1 - Catálogos:"
    echo "   • Niveles de Dificultad: 5 registros"
    echo "   • Categorías de Programa: 5 registros"
    echo "   • Tipos de Programa: 5 registros"
    echo "   • Equipamiento: 10 registros"
    echo "   • Grupos Musculares: 7 registros"
    echo "   • Tipos de Evaluación: 5 registros"
    echo "   • Tipos de Meta: 6 registros"
    echo ""
    echo "   FASE 2 - Usuarios y Ejercicios:"
    echo "   • Usuarios de Prueba: 3 registros"
    echo "   • Ejercicios: 10 registros"
    echo ""
    echo "   FASE 3 - Estructura de Entrenamiento:"
    echo "   • Ejercicios Adicionales: 4 registros"
    echo "   • Programas de Entrenamiento: 2 registros"
    echo "   • Workouts/Entrenamientos: 3 registros"
    echo "   • Líneas de Ejercicio: 11 registros"
    echo ""
    echo "   FASE 4 - Inscripciones de Usuario a Programas:"
    echo "   • Programa Adicional: 1 registro"
    echo "   • Inscripciones de Usuario: 6 registros"
    echo ""
    echo "   FASE 5 - Seguimiento Corporal y Evaluaciones:"
    echo "   • Mediciones Corporales: 4 registros"
    echo "   • Evaluaciones Físicas: 8 registros"
    echo ""
    echo "   FASE 6 - Seguimiento de Nutrición:"
    echo "   • Biblioteca de Alimentos: 8 registros"
    echo "   • Registros de Comidas: 5 registros"
    echo "   • Líneas de Alimentos: 13 registros"
    echo ""
    echo "   FASE 7 - Establecimiento de Metas:"
    echo "   • Metas de Fitness: 8 registros"
    echo ""
    echo "   FASE 8 - Registro de Entrenamientos Realizados:"
    echo "   • Historial de Entrenamientos: 5 registros"
    echo "   • Rendimiento de Ejercicios: 17 registros"
    echo ""
    echo "   FASE 9 - Sistema de Logros:"
    echo "   • Biblioteca de Logros: 8 registros"
    echo "   • Logros Obtenidos por Usuarios: 8 registros"
    echo ""
    echo "   FASE 10 - Protocolos de Usuario:"
    echo "   • Protocolos Personalizados: 5 registros"
    echo ""
    echo "   FASE 11 - Integración con Suscripciones (NUEVA):"
    echo "   • Productos de Suscripción: 3 registros (Básico, Premium, VIP)"
    echo "   • Plantillas de Suscripción: 3 registros"
    echo "   • Suscripciones Activas de Usuarios: 3 registros"
    echo "   • Vinculación Programas-Suscripciones: 3 programas configurados"
    echo ""
    echo "🎉 ¡SEMILLADO COMPLETO V2! Integración con suscripciones de Odoo implementada."
    echo ""
    echo "🌐 Puedes verificar los datos en:"
    echo "   http://localhost:8069"
    echo ""
    echo "📋 Menús disponibles:"
    echo "   • Fitness → Catálogos → [Todos los catálogos]"
    echo "   • Fitness → Ejercicios → Biblioteca de Ejercicios"
    echo "   • Contactos → [Ver usuarios con datos de fitness]"
else
    echo "❌ Error al aplicar el semillado"
    exit 1
fi 