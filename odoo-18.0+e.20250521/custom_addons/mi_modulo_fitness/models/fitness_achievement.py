# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessAchievement(models.Model):
    _name = 'fitness.achievement'
    _description = 'Definición de Logro o Hazaña de Fitness'
    _order = 'name'

    name = fields.Char(string="Nombre del Logro", required=True, translate=True)
    description = fields.Text(string="Descripción del Logro", translate=True, help="Qué representa este logro y por qué es importante.")
    
    # Para V1, los criterios y recompensas son descriptivos.
    # La lógica de asignación automática sería para V2.
    criteria_description = fields.Text(
        string="Criterios para Obtener (Descripción)", 
        help="Descripción textual de cómo se obtiene este logro. Ej: Completar el primer programa, levantar X peso, etc."
    )
    reward_description = fields.Text(
        string="Recompensa (Descripción)", 
        help="Descripción de la recompensa o reconocimiento. Ej: Medalla virtual, puntos extra, mención especial."
    )
    
    image_1920 = fields.Image(
        string="Icono/Imagen del Logro", 
        max_width=512, max_height=512, 
        help="Imagen visual para representar el logro (ej. una medalla)."
    )
    
    active = fields.Boolean(
        string="Activo", 
        default=True, 
        help="Si el logro está activo y puede ser asignado."
    )
    
    # Campo para agrupar o categorizar logros si es necesario en el futuro
    # achievement_category_id = fields.Many2one('fitness.achievement.category', string="Categoría de Logro")


class FitnessUserAchievement(models.Model):
    _name = 'fitness.user.achievement'
    _description = 'Logro Obtenido por un Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para notificar al usuario quizás
    _order = 'user_id, date_achieved desc'

    name = fields.Char(string="Referencia", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # O 'restrict'
        index=True,
        tracking=True
    )
    achievement_id = fields.Many2one(
        comodel_name='fitness.achievement',
        string="Logro Obtenido",
        required=True,
        ondelete='restrict', # No borrar una definición de logro si ya fue asignada
        tracking=True
    )
    
    date_achieved = fields.Date(
        string="Fecha de Obtención",
        required=False,
        tracking=True,
        help="Fecha en que se obtuvo el logro. Vacío si está en progreso."
    )
    
    # Para V1, el estado y progreso son principalmente para registro manual por el entrenador.
    status = fields.Selection([
        ('locked', 'Bloqueado / No Iniciado'),
        ('in_progress', 'En Progreso'), # Si el entrenador quiere marcar un progreso manual
        ('achieved', 'Logrado')
    ], string="Estado", default='achieved', tracking=True, help="Para V1, usualmente se registrará como 'Logrado'.")

    # Progreso manual (descriptivo para V1)
    progress_manual_notes = fields.Text(
        string="Notas de Progreso (Manual)",
        help="Descripción del progreso actual si el estado es 'En Progreso'."
    )

    trainer_notes = fields.Text(
        string="Notas del Entrenador",
        help="Comentarios del entrenador al asignar el logro."
    )

    @api.depends('user_id.name', 'achievement_id.name', 'date_achieved')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            achievement_name = record.achievement_id.name if record.achievement_id else "N/D"
            if record.date_achieved:
                date_str = fields.Date.to_string(record.date_achieved)
                record.name = f"Logro: {user_name} - {achievement_name} ({date_str})"
            else:
                record.name = f"Logro en Progreso: {user_name} - {achievement_name}" 