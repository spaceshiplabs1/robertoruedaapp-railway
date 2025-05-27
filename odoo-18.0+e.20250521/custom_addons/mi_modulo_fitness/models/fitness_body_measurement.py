# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessBodyMeasurement(models.Model):
    _name = 'fitness.body.measurement'
    _description = "Registro de Mediciones Corporales del Usuario"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial si es necesario
    _order = 'user_id, date desc' # Ordenar por usuario, luego fecha más reciente primero

    name = fields.Char(string="Referencia", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # Considera 'restrict'
        index=True,
        tracking=True
    )
    date = fields.Date(
        string="Fecha de Medición",
        required=True,
        default=fields.Date.context_today,
        index=True,
        tracking=True
    )

    # Asumimos unidades consistentes (ej. kg para peso, cm para circunferencias)
    # Se podría añadir un campo 'unit_system' ('metric', 'imperial') en res.partner o config general
    weight = fields.Float(string="Peso", tracking=True, help="Peso en la unidad de medida del sistema (ej. kg)")

    # Circunferencias
    chest = fields.Float(string="Pecho", tracking=True, help="Circunferencia del Pecho (ej. cm)")
    waist = fields.Float(string="Cintura", tracking=True, help="Circunferencia de la Cintura (ej. cm)")
    hips = fields.Float(string="Caderas", tracking=True, help="Circunferencia de las Caderas (ej. cm)")
    
    # Mediciones adicionales opcionales (puedes añadir más según necesidad)
    left_arm = fields.Float(string="Brazo Izquierdo (contraído)", tracking=True)
    right_arm = fields.Float(string="Brazo Derecho (contraído)", tracking=True)
    left_thigh = fields.Float(string="Muslo Izquierdo (parte media)", tracking=True)
    right_thigh = fields.Float(string="Muslo Derecho (parte media)", tracking=True)
    # neck = fields.Float(string="Cuello", tracking=True)
    # left_calf = fields.Float(string="Pantorrilla Izquierda", tracking=True)
    # right_calf = fields.Float(string="Pantorrilla Derecha", tracking=True)

    body_fat_percentage = fields.Float(
        string="Grasa Corporal (%)",
        tracking=True,
        help="Porcentaje de grasa corporal (si se mide)."
    )

    measurement_picture = fields.Image(
        string="Foto de Progreso (de esta medición)",
        max_width=1920, max_height=1920,
        help="Foto opcional del usuario en la fecha de esta medición."
    )

    notes = fields.Text(
        string="Notas Adicionales",
        help="Condiciones de la medición, cómo se siente el usuario, etc."
    )

    # Podría estar vinculado a una inscripción de programa si las mediciones son parte de un seguimiento estructurado
    # user_program_id = fields.Many2one('fitness.user.program', string="Asociado a Inscripción de Programa")


    @api.depends('user_id.name', 'date')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            date_str = fields.Date.to_string(record.date) if record.date else "N/D"
            record.name = f"Medición: {user_name} - {date_str}" 