# -*- coding: utf-8 -*-

from odoo import models, fields

class FitnessWorkoutLine(models.Model):
    _name = 'fitness.workout.line'
    _description = 'Línea/Componente de Ejercicio dentro de un Entrenamiento'
    _order = 'workout_id, sequence, id' # Ordenar por entrenamiento, luego por secuencia propia

    workout_id = fields.Many2one(
        comodel_name='fitness.workout',
        string="Entrenamiento Principal",
        required=True,
        ondelete='cascade', # Si se borra el entrenamiento, sus líneas también
        index=True
    )
    exercise_id = fields.Many2one(
        comodel_name='fitness.exercise',
        string="Ejercicio",
        required=True,
        ondelete='restrict', # No permitir borrar un ejercicio si está en uso aquí
        index=True
    )

    sequence = fields.Integer(
        string="Orden/Paso",
        default=10,
        help="Secuencia de este ejercicio/bloque dentro del entrenamiento."
    )

    # Definición de Series, Repeticiones, Descanso para la plantilla del workout
    # Usamos campos de texto para flexibilidad (ej. "8-12 reps", "AMRAP 10 min", "60-90s")
    sets_text = fields.Char(
        string="Series",
        help="Número o descripción de las series. Ej: 3, 4, Calentamiento: 2"
    )
    repetitions_text = fields.Char(
        string="Repeticiones / Duración",
        help="Rango de repeticiones o tiempo. Ej: 8-12, 15, AMRAP, 30s, Hasta el fallo."
    )
    rest_period_text = fields.Char(
        string="Descanso entre Series",
        help="Tiempo de descanso. Ej: 60s, 90-120s, Mínimo necesario."
    )
    
    # Tempo (si se usa frecuentemente, podría ser un campo separado)
    # tempo_text = fields.Char(string="Tempo", help="Ej: 2-0-1-0 (excéntrica-pausa-concéntrica-pausa)")

    special_instructions = fields.Text(
        string="Instrucciones Especiales / Técnica",
        help="Notas específicas sobre la ejecución, técnica, o enfoque para este ejercicio en este entrenamiento."
    )

    # Este modelo define la ESTRUCTURA del entrenamiento.
    # El rendimiento real (pesos, reps exactas, etc.) se registrará en 'fitness.exercise.performance'. 