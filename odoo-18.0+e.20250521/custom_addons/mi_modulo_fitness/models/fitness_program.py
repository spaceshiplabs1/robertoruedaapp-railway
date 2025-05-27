# -*- coding: utf-8 -*-

from odoo import models, fields

class FitnessProgram(models.Model):
    _name = 'fitness.program'
    _description = 'Programa de Entrenamiento Fitness'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial de cambios y actividades

    name = fields.Char(string="Nombre del Programa", required=True, tracking=True)
    description = fields.Text(string="Descripción Detallada")
    
    difficulty_id = fields.Many2one(
        comodel_name='fitness.difficulty', 
        string="Nivel de Dificultad", 
        tracking=True,
        ondelete='restrict' # No permitir borrar dificultad si está usada en un programa
    )
    program_category_id = fields.Many2one(
        comodel_name='fitness.program.category', 
        string="Categoría del Programa", 
        tracking=True,
        ondelete='restrict'
    )
    program_type_id = fields.Many2one(
        comodel_name='fitness.program.type', 
        string="Tipo de Programa", 
        tracking=True,
        ondelete='restrict'
    )
    
    duration_text = fields.Char(
        string="Duración del Programa", 
        help="Ej: 4 Semanas, Ciclo Continuo, 90 Días"
    )

    privacy_setting = fields.Selection([
        ('public', 'Público'),
        ('private', 'Privado (Solo para uso interno del entrenador/admin)')
    ], string="Visibilidad", default='private', required=True, tracking=True)

    autosync_user_schedule = fields.Boolean(
        string="¿Sincronización Automática con Horario de Usuario?", 
        default=False, 
        help="Marcar si el programa debe tener lógica futura para auto-asignarse al calendario del usuario."
    )

    required_equipment_ids = fields.Many2many(
        comodel_name='fitness.equipment',                
        relation='fitness_program_equipment_rel',    
        column1='program_id',                       
        column2='equipment_id',                     
        string="Equipamiento Requerido"
    )
    
    # Integración con Suscripciones de Odoo
    allowed_subscription_product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='fitness_program_subscription_rel',
        column1='program_id',
        column2='product_id',
        string="Planes de Suscripción que dan Acceso",
        domain="['|', ('recurring_invoice', '=', True), '&', ('recurring_invoice', '=', False), ('name', 'ilike', 'fitness')]",  # Productos de suscripción o productos fitness gratuitos
        help="Selecciona los planes de suscripción que permitirán al usuario acceder a este programa."
    )

    # Campos relacionales (el otro lado de la relación se define en los otros modelos)
    workout_ids = fields.One2many(
        comodel_name='fitness.workout', 
        inverse_name='program_id', 
        string="Entrenamientos del Programa"
    )
    user_enrollment_ids = fields.One2many(
        comodel_name='fitness.user.program', 
        inverse_name='program_id', 
        string="Inscripciones de Usuarios"
    )
    
    active = fields.Boolean(
        string="Activo", 
        default=True, 
        help="Desmarcar para archivar el programa y que no esté disponible para nuevas inscripciones."
    )
    image_1920 = fields.Image(string="Imagen Principal", max_width=1920, max_height=1920)
    sequence = fields.Integer(string="Secuencia de Orden", default=10)

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "El nombre del programa ya existe y debe ser único.")
    # ] 