# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessUserProtocol(models.Model):
    _name = 'fitness.user.protocol'
    _description = "Protocolo de Estilo de Vida/Recuperación Asignado al Usuario"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'user_id, start_date desc, is_active_protocol desc'

    name = fields.Char(string="Referencia del Protocolo", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # O 'restrict'
        index=True,
        tracking=True
    )
    
    is_active_protocol = fields.Boolean(
        string="¿Protocolo Activo Principal?",
        default=True,
        tracking=True,
        help="Marcar si este es el conjunto de protocolos que el usuario está siguiendo activamente. "
             "Se recomienda gestionar para que solo haya un protocolo activo a la vez por usuario."
    )

    start_date = fields.Date(
        string="Fecha de Inicio del Protocolo",
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    end_date = fields.Date(
        string="Fecha de Fin del Protocolo (Opcional)",
        tracking=True,
        help="Dejar en blanco si es indefinido o hasta nueva indicación."
    )

    # Descripciones de los protocolos específicos (campos de Texto para flexibilidad en V1)
    fasting_protocol_description = fields.Text(
        string="Protocolo de Ayuno", 
        help="Ej: '16:8 diario (ventana de alimentación 12pm-8pm)', 'Ayuno de 24h los lunes'."
    )
    sauna_steam_protocol_description = fields.Text(
        string="Protocolo de Sauna / Baño de Vapor",
        help="Ej: 'Sauna infrarroja 3x semana, 20 min', 'Vapor después de entrenamientos de fuerza'."
    )
    cold_exposure_protocol_description = fields.Text(
        string="Protocolo de Exposición al Frío",
        help="Ej: 'Duchas frías matutinas (final 2-3 min)', 'Inmersión en hielo 1x semana, 5 min a 10°C'."
    )
    sleep_recovery_protocol_description = fields.Text(
        string="Protocolo de Sueño y Recuperación",
        help="Ej: 'Acostarse a las 10pm, despertar 6am. No cafeína después de las 2pm. Habitación oscura y fresca.'."
    )
    daily_movement_protocol_description = fields.Text(
        string="Protocolo de Movimiento Diario (NEAT)",
        help="Ej: 'Objetivo: 10,000-12,000 pasos diarios. Subir escaleras en lugar de ascensor.'."
    )
    hydration_protocol_description = fields.Text(
        string="Protocolo de Hidratación",
        help="Ej: 'Mínimo 3 litros de agua al día. Considerar electrolitos en días de mucho calor o sudoración'."
    )
    stress_management_protocol_description = fields.Text(
        string="Protocolo de Manejo de Estrés",
        help="Ej: 'Meditación diaria 10 min (mañana)', 'Técnicas de respiración', 'Journaling'."
    )
    
    other_recommendations = fields.Text(
        string="Otras Recomendaciones / Notas Generales del Protocolo",
        help="Suplementación específica, hábitos adicionales, recursos recomendados, etc."
    )

    @api.depends('user_id.name', 'start_date', 'is_active_protocol')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            date_str = fields.Date.to_string(record.start_date) if record.start_date else "N/D"
            active_status = " (Activo)" if record.is_active_protocol else ""
            record.name = f"Protocolo: {user_name} - {date_str}{active_status}"

    # Consideración para V2: Lógica para asegurar que solo un protocolo esté activo por usuario,
    # o un sistema de versionado/historial de protocolos más explícito si cambian frecuentemente.
    # Por ahora, 'is_active_protocol' y las fechas ayudan a gestionarlo manualmente. 