# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessWorkoutHistory(models.Model):
    _name = 'fitness.workout.history'
    _description = "Historial de Entrenamientos Completados por el Usuario"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'user_id, completion_datetime desc' # Ordenar por usuario, luego fecha más reciente

    name = fields.Char(string="Referencia de Sesión", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # O 'restrict', según política de borrado
        index=True,
        tracking=True
    )
    workout_definition_id = fields.Many2one(
        comodel_name='fitness.workout',
        string="Entrenamiento Realizado (Plantilla)",
        required=True, 
        ondelete='restrict', # No borrar una plantilla de workout si tiene historiales
        tracking=True,
        help="El entrenamiento planificado que el usuario realizó."
    )
    user_program_id = fields.Many2one(
        comodel_name='fitness.user.program',
        string="Inscripción al Programa (Contexto)",
        ondelete='set null', # Si se borra la inscripción, el historial permanece pero sin este enlace
        tracking=True,
        help="Opcional: La inscripción al programa bajo la cual se realizó este entrenamiento."
    )

    completion_datetime = fields.Datetime(
        string="Fecha y Hora de Finalización",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
        index=True
    )
    actual_duration_minutes = fields.Integer(
        string="Duración Real de la Sesión (minutos)",
        tracking=True,
        help="Tiempo total que el usuario dedicó a esta sesión de entrenamiento."
    )

    user_rating = fields.Selection([
        ('1', '1 - Muy Malo'),
        ('2', '2 - Malo'),
        ('3', '3 - Regular'),
        ('4', '4 - Bueno'),
        ('5', '5 - Excelente')
    ], string="Calificación General de la Sesión", tracking=True)

    difficulty_feedback = fields.Selection([
        ('too_easy', 'Demasiado Fácil'),
        ('just_right', 'Adecuado / Justo lo Esperado'),
        ('challenging', 'Desafiante (pero lograble)'),
        ('too_hard', 'Demasiado Difícil'),
        ('modified_significantly', 'Modificado Significativamente'),
        ('incomplete', 'Incompleto')
    ], string="Percepción de Dificultad de la Sesión", tracking=True)
    
    user_session_notes = fields.Text(
        string="Notas del Usuario sobre la Sesión",
        help="Comentarios del usuario: cómo se sintió, energía, logros, problemas, etc."
    )
    
    # Líneas de rendimiento de cada ejercicio en esta sesión
    exercise_performance_ids = fields.One2many(
        comodel_name='fitness.exercise.performance', # Modelo del Punto #8 (se definirá a continuación)
        inverse_name='workout_history_id',
        string="Rendimiento Detallado de Ejercicios",
        copy=True 
    )

    # Campos adicionales que podrían ser útiles (quizás para V2 o si son simples)
    # location_type = fields.Selection([('gym','Gimnasio'), ('home','Casa'), ('outdoors','Exterior'), ('other','Otro')], string="Lugar")
    # perceived_exertion_rpe = fields.Integer(string="RPE (1-10)", help="Tasa de Esfuerzo Percibido general de la sesión")

    @api.depends('user_id.name', 'workout_definition_id.name', 'completion_datetime')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            workout_name = record.workout_definition_id.name if record.workout_definition_id else "N/D"
            date_str = fields.Datetime.context_timestamp(record, record.completion_datetime).strftime('%Y-%m-%d %H:%M') if record.completion_datetime else "N/D"
            record.name = f"Historial: {user_name} - {workout_name} ({date_str})" 