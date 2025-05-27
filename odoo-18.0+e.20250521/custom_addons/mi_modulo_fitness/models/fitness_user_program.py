# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FitnessUserProgram(models.Model):
    _name = 'fitness.user.program'
    _description = "Inscripción y Progreso de Usuario en Programa de Entrenamiento"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'user_id, start_date desc' # Ordenar por usuario, luego fecha de inicio descendente

    name = fields.Char(string="Referencia de Inscripción", compute='_compute_name', store=True, readonly=True)

    user_id = fields.Many2one(
        comodel_name='res.partner',
        string="Usuario",
        required=True,
        ondelete='cascade', # Considera 'restrict' si prefieres no borrar inscripciones al borrar un usuario
        index=True,
        tracking=True,
        domain="[('is_company', '=', False)]" # Dominio: solo personas (no empresas)
    )
    program_id = fields.Many2one(
        comodel_name='fitness.program',
        string="Programa de Entrenamiento",
        required=True,
        ondelete='restrict', # No permitir borrar un programa si tiene inscripciones
        index=True,
        tracking=True
    )

    enrollment_status = fields.Selection([
        ('active', 'Activa'),
        ('paused', 'Pausada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('pending_start', 'Pendiente de Inicio')
    ], string="Estado de la Inscripción", default='pending_start', required=True, tracking=True)

    start_date = fields.Date(string="Fecha de Inicio Programada/Real", default=fields.Date.context_today, tracking=True)
    end_date = fields.Date(string="Fecha de Finalización Estimada/Real", tracking=True)

    completion_percentage = fields.Float(
        string="Progreso (%)",
        default=0.0,
        tracking=True,
        aggregator="avg", # Para agregación en vistas de Odoo si se usan
        help="Porcentaje de finalización del programa. Idealmente calculado."
        # compute='_compute_completion_percentage', store=True # La lógica de cálculo se definirá después
    )

    initial_enrollment_picture = fields.Image(
        string="Foto Inicial (al Inscribirse)",
        max_width=1920, max_height=1920,
        help="Foto del usuario al iniciar este programa específico."
    )
    current_progress_picture = fields.Image(
        string="Foto de Progreso Actual",
        max_width=1920, max_height=1920,
        help="Foto más reciente del progreso del usuario en este programa."
    )

    trainer_notes = fields.Text(string="Notas del Entrenador (sobre esta inscripción)")
    user_feedback = fields.Text(string="Feedback del Usuario (sobre el programa)")

    # Relación a los entrenamientos completados por este usuario para este programa
    # workout_history_ids = fields.One2many('fitness.workout.history', 'user_program_id', string="Historial de Entrenamientos Realizados")


    _sql_constraints = [
        ('user_program_start_date_uniq', 'unique (user_id, program_id, start_date)', 
         "Un usuario no puede tener múltiples inscripciones al mismo programa con la misma fecha de inicio.")
    ]

    @api.depends('user_id.name', 'program_id.name')
    def _compute_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            program_name = record.program_id.name if record.program_id else "N/D"
            record.name = f"Inscripción: {user_name} - {program_name}"

    # def _compute_completion_percentage(self):
    #     for record in self:
    #         # Lógica futura para calcular el porcentaje de completitud
    #         # basada en record.workout_history_ids y los workouts definidos en record.program_id.workout_ids
    #         record.completion_percentage = 0.0 # Placeholder

    @api.model_create_multi
    def create(self, vals_list):
        """Override create para validar acceso basado en suscripción antes de crear la inscripción"""
        # Validar acceso basado en suscripción antes de crear (compatible con batch)
        for vals in vals_list:
            if 'user_id' in vals and 'program_id' in vals:
                self._validate_subscription_access(vals['user_id'], vals['program_id'])
        return super(FitnessUserProgram, self).create(vals_list)

    def write(self, vals):
        """Override write para validar acceso si se cambia usuario o programa"""
        # Si se está cambiando el usuario o programa, validar acceso
        for record in self:
            user_id = vals.get('user_id', record.user_id.id)
            program_id = vals.get('program_id', record.program_id.id)
            if 'user_id' in vals or 'program_id' in vals:
                self._validate_subscription_access(user_id, program_id)
        return super(FitnessUserProgram, self).write(vals)

    def _validate_subscription_access(self, user_id, program_id):
        """
        Valida si el usuario tiene una suscripción activa que le permita acceso al programa
        """
        # Obtener el programa y sus suscripciones permitidas
        program = self.env['fitness.program'].browse(program_id)
        
        # Si el programa no tiene restricciones de suscripción, permitir acceso
        if not program.allowed_subscription_product_ids:
            return True
            
        # Buscar suscripciones activas del usuario
        user = self.env['res.partner'].browse(user_id)
        
        # Buscar suscripciones activas del usuario en el módulo de suscripciones de Odoo 18
        active_subscriptions = self.env['sale.order'].search([
            ('partner_id', '=', user_id),
            ('is_subscription', '=', True),
            ('subscription_state', 'in', ['3_progress', '4_paused']),  # Suscripciones activas
        ])
        
        # Verificar si alguna suscripción activa incluye productos que dan acceso al programa
        user_subscription_products = active_subscriptions.mapped('order_line.product_template_id')
        allowed_products = program.allowed_subscription_product_ids
        
        # Verificar si hay intersección entre productos de suscripción del usuario y productos permitidos
        if not (set(user_subscription_products.ids) & set(allowed_products.ids)):
            raise ValidationError(
                f"El usuario {user.name} no tiene una suscripción activa que permita acceso al programa '{program.name}'. "
                f"Planes requeridos: {', '.join(allowed_products.mapped('name'))}"
            )
        
        return True

    @api.model
    def check_user_program_access(self, user_id, program_id):
        """
        Método público para verificar acceso sin crear inscripción
        Útil para validaciones en frontend
        """
        try:
            self._validate_subscription_access(user_id, program_id)
            return {'has_access': True, 'message': 'Acceso permitido'}
        except ValidationError as e:
            return {'has_access': False, 'message': str(e)} 