# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessGoal(models.Model):
    _name = 'fitness.goal'
    _description = "Meta de Fitness del Usuario"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'user_id, target_date desc, name' # Ordenar por usuario, fecha objetivo y nombre

    name = fields.Char(
        string="Nombre Corto de la Meta", 
        required=True, 
        tracking=True,
        help="Un título breve y descriptivo para la meta, ej: 'Perder 5kg', 'Correr Maratón Sub-4h'"
    )
    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # O 'restrict'
        index=True,
        tracking=True
    )
    goal_type_id = fields.Many2one(
        comodel_name='fitness.goal.type', # Modelo definido en fitness_catalogs.py
        string="Tipo de Meta",
        required=True,
        ondelete='restrict', # No borrar tipo de meta si está en uso
        tracking=True
    )
    description = fields.Text(
        string="Descripción Detallada / Motivación",
        help="Más detalles sobre la meta: por qué es importante para el usuario, estrategias, etc."
    )
    
    start_date = fields.Date(
        string="Fecha de Inicio de la Meta",
        default=fields.Date.context_today,
        tracking=True
    )
    target_date = fields.Date(
        string="Fecha Objetivo para la Meta",
        tracking=True,
        help="Fecha límite estimada o deseada para alcanzar esta meta."
    )

    status = fields.Selection([
        ('not_started', 'No Iniciada'),
        ('in_progress', 'En Progreso'),
        ('achieved', 'Lograda'),
        ('partially_achieved', 'Parcialmente Lograda'),
        ('on_hold', 'En Pausa'),
        ('re_evaluating', 'Re-evaluando'),
        ('cancelled', 'Cancelada (Abandonada)'),
        ('failed', 'No Lograda (Fecha objetivo pasada)')
    ], string="Estado Actual de la Meta", default='not_started', required=True, tracking=True, copy=False)

    # Para V1, la métrica y el objetivo son descriptivos.
    # En V2 se podría estructurar más con valores numéricos, iniciales, actuales, etc.
    target_metric_description = fields.Text(
        string="Objetivo Específico y Medible",
        required=True,
        help="Describe claramente qué se quiere lograr y cómo se medirá. Ej:\n"
             "- 'Reducir el peso corporal de 85kg a 78kg.'\n"
             "- 'Aumentar las repeticiones en dominadas de 5 a 10.'\n"
             "- 'Completar consistentemente 3 sesiones de cardio de 30 minutos por semana durante 1 mes.'\n"
             "- 'Mejorar el tiempo de carrera de 5K de 30 minutos a 27 minutos.'"
    )

    # Notas para el seguimiento manual del progreso en V1
    progress_notes = fields.Text(
        string="Notas de Progreso y Actualizaciones",
        help="Registro de avances, obstáculos, ajustes realizados, etc."
    )
    
    # Resultado final o reflexión al cambiar el estado a Lograda, Cancelada o No Lograda
    outcome_summary = fields.Text(string="Resumen del Resultado / Reflexión Final")

    # Un campo calculado para el nombre completo podría ser útil para visualización,
    # aunque 'name' ya es un buen descriptor.
    # display_name = fields.Char(compute='_compute_display_name', store=True)
    # @api.depends('name', 'user_id.name')
    # def _compute_display_name(self):
    #     for record in self:
    #         record.display_name = f"{record.user_id.name or 'N/A'} - {record.name or 'Meta sin título'}" 