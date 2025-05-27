# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessExercisePerformance(models.Model):
    _name = 'fitness.exercise.performance'
    _description = "Rendimiento Detallado de un Ejercicio en una Sesión"
    _order = 'workout_history_id, sequence, id' # Ordenar por sesión, luego secuencia del ejercicio

    name = fields.Char(string="Referencia de Rendimiento", compute='_compute_name', store=True, readonly=True)

    workout_history_id = fields.Many2one(
        comodel_name='fitness.workout.history',
        string="Sesión de Entrenamiento Registrada",
        required=True,
        ondelete='cascade', # Si se borra el historial, se borran sus líneas de rendimiento
        index=True
    )
    exercise_id = fields.Many2one(
        comodel_name='fitness.exercise',
        string="Ejercicio Realizado",
        required=True,
        ondelete='restrict', # No borrar un ejercicio de la biblioteca si tiene registros de rendimiento
        index=True
    )
    
    # Opcional: Enlace a la línea específica del workout planificado para comparar plan vs realidad
    workout_line_id = fields.Many2one(
        comodel_name='fitness.workout.line',
        string="Línea Planificada (Opcional)",
        ondelete='set null', # Si se borra la línea del plan, el rendimiento permanece
        help="Referencia a la línea del entrenamiento planificado, si aplica."
    )

    sequence = fields.Integer(
        string="Orden en Sesión",
        default=10,
        help="Secuencia en la que se realizó este ejercicio dentro de la sesión."
    )

    # Campos para registrar el rendimiento real. Usamos Char para flexibilidad en V1.
    # Esto permite al usuario anotar variaciones por serie si lo desea.
    sets_completed_text = fields.Char(
        string="Series Realizadas", 
        help="Ej: '3', 'Todas', '2 (fatiga)'."
    )
    reps_completed_text = fields.Char(
        string="Repeticiones por Serie", 
        help="Ej: '10, 9, 8', '12 (todas)', 'AMRAP: 15 reps'."
    )
    weights_used_text = fields.Char(
        string="Peso Utilizado por Serie (o Resistencia)", 
        help="Ej: '50kg, 50kg, 52.5kg', 'Peso Corporal', 'Banda elástica roja'."
    )
    
    # Para ejercicios basados en tiempo
    duration_seconds_completed = fields.Integer(
        string="Duración Realizada (segundos)",
        help="Tiempo total para ejercicios basados en duración, ej: plancha, cardio."
    )

    difficulty_perception_exercise = fields.Selection([
        ('1_very_easy', '1 - Muy Fácil'),
        ('2_easy', '2 - Fácil'),
        ('3_moderate', '3 - Moderado (RPE 5-6)'),
        ('4_hard', '4 - Difícil (RPE 7-8)'),
        ('5_very_hard', '5 - Muy Difícil / Al fallo (RPE 9-10)')
    ], string="Percepción de Dificultad (Ejercicio)", help="Qué tan difícil se sintió este ejercicio en particular.")
    
    progress_notes_exercise = fields.Text(
        string="Notas Específicas del Ejercicio",
        help="Comentarios sobre la forma, sensaciones, puntos a mejorar, etc., para este ejercicio en esta sesión."
    )
    
    # Si se quisiera un detalle por serie (más complejo, quizás V2):
    # performance_set_ids = fields.One2many('fitness.exercise.performance.set', 'exercise_performance_id', string="Detalle de Series")

    @api.depends('workout_history_id.name', 'exercise_id.name', 'sequence')
    def _compute_name(self):
        for record in self:
            # Intenta obtener nombres descriptivos, si no existen, usa "N/D" o similar.
            hist_display_name = record.workout_history_id.name if record.workout_history_id else "Sesión N/D"
            exercise_display_name = record.exercise_id.name if record.exercise_id else "Ejercicio N/D"
            record.name = f"Rend: {exercise_display_name} (Paso {record.sequence}) en [{hist_display_name}]" 