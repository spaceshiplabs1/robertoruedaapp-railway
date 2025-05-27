# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessAssessment(models.Model):
    _name = 'fitness.assessment'
    _description = "Registro de Prueba de Evaluación Física del Usuario"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'user_id, date desc, assessment_type_id' # Ordenar por usuario, fecha y tipo

    name = fields.Char(string="Referencia de Evaluación", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # O 'restrict', según la política de borrado de usuarios
        index=True,
        tracking=True
    )
    assessment_type_id = fields.Many2one(
        comodel_name='fitness.assessment.type',
        string="Tipo de Prueba de Evaluación",
        required=True,
        ondelete='restrict', # No permitir borrar un tipo de prueba si tiene resultados registrados
        tracking=True,
        index=True
    )
    date = fields.Date(
        string="Fecha de Realización",
        required=True,
        default=fields.Date.context_today,
        index=True,
        tracking=True
    )

    # Resultados de la prueba
    value_numerical = fields.Float(
        string="Resultado Numérico",
        tracking=True,
        help="Valor cuantitativo de la prueba. La unidad de medida se define en el Tipo de Prueba."
    )
    value_text = fields.Char( # Usar Char para texto corto, o Text para más largo
        string="Resultado Textual / Observación Corta",
        tracking=True,
        help="Para resultados cualitativos, ej: 'Aprobado', 'Necesita mejorar X', o una puntuación simple como 'A+'."
    )
    
    notes = fields.Text(
        string="Notas Detalladas de la Evaluación",
        help="Contexto de la prueba, cómo se sintió el usuario, equipamiento específico usado, comentarios del evaluador, etc."
    )

    # Opcional: Imagen o video corto como evidencia o para análisis de forma.
    # assessment_media = fields.Binary(string="Archivo Multimedia (Foto/Video Evidencia)")
    assessment_picture = fields.Image(string="Foto Evidencia (Opcional)", max_width=1920, max_height=1920)


    # Opcional: Si la evaluación está directamente ligada a una fase o momento de un programa inscrito.
    # user_program_id = fields.Many2one(
    #     comodel_name='fitness.user.program',
    #     string="Asociado a Inscripción de Programa",
    #     help="Vincular esta evaluación a una inscripción de programa específica del usuario."
    # )

    @api.depends('user_id.name', 'assessment_type_id.name', 'date')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            type_name = record.assessment_type_id.name if record.assessment_type_id else "N/D"
            date_str = fields.Date.to_string(record.date) if record.date else "N/D"
            record.name = f"Eval: {user_name} - {type_name} ({date_str})" 