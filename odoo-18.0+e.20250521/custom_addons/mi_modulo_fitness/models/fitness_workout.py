# -*- coding: utf-8 -*-

from odoo import models, fields

class FitnessWorkout(models.Model):
    _name = 'fitness.workout'
    _description = 'Entrenamiento (Sesión Específica dentro de un Programa)'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'program_id, sequence_in_program, name'

    name = fields.Char(string="Nombre del Entrenamiento", required=True, tracking=True)
    description = fields.Text(string="Descripción General del Entrenamiento")

    program_id = fields.Many2one(
        comodel_name='fitness.program',
        string="Programa al que Pertenece",
        required=True,
        ondelete='cascade', # Si se borra el programa, se borran sus entrenamientos
        index=True, # Es común buscar/filtrar por programa
        tracking=True
    )

    # Posición dentro del programa (ej. Día 1, Sesión A, etc.)
    # Usamos un campo de secuencia para flexibilidad.
    sequence_in_program = fields.Integer(
        string="Orden/Secuencia en Programa",
        default=10,
        help="Define el orden de este entrenamiento dentro de su programa (ej. 10, 20, 30...)."
    )
    
    estimated_duration_minutes = fields.Integer(
        string="Duración Estimada (minutos)",
        help="Tiempo total aproximado para completar el entrenamiento en minutos."
    )

    workout_type = fields.Selection([
        ('standard', 'Estándar (Bloques de Ejercicios)'),
        ('circuit', 'Circuito'),
        ('amrap', 'AMRAP (Tantas Rondas/Repeticiones Como Sea Posible)'),
        ('emom', 'EMOM (Cada Minuto en el Minuto)'),
        ('tabata', 'Tábata'),
        ('recovery', 'Recuperación / Movilidad'),
        ('other', 'Otro')
    ], string="Tipo de Entrenamiento", default='standard', required=True, tracking=True)

    # Líneas que componen este entrenamiento (ejercicios, series, reps, etc.)
    workout_line_ids = fields.One2many(
        comodel_name='fitness.workout.line', 
        inverse_name='workout_id', 
        string="Líneas de Ejercicio del Entrenamiento",
        copy=True # Si se duplica el entrenamiento, también duplicar sus líneas
    )
    
    active = fields.Boolean(
        string="Activo", 
        default=True, 
        help="Desmarcar para archivar este entrenamiento."
    )
    
    internal_notes = fields.Text(
        string="Notas Internas (Entrenador)",
        help="Notas solo visibles para el entrenador o administradores."
    )
    user_facing_notes = fields.Text(
        string="Instrucciones/Notas para el Usuario",
        help="Instrucciones o consejos especiales para el usuario para este entrenamiento."
    ) 