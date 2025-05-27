# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartnerExtension(models.Model):
    _inherit = 'res.partner'

    # Campos personalizados para la información del fitness del usuario
    date_of_birth = fields.Date(string="Fecha de Nacimiento")
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro')
    ], string="Género")
    
    account_fitness_status = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('pending_payment', 'Pago Pendiente'),
        ('trial', 'Prueba')
    ], string="Estado de Cuenta Fitness", default='active', tracking=True)

    height_cm = fields.Float(string="Altura (cm)", help="Altura del usuario en centímetros")

    activity_level = fields.Selection([
        ('sedentary', 'Sedentario (poco o ningún ejercicio)'),
        ('light', 'Ligero (ejercicio ligero 1-3 días/semana)'),
        ('moderate', 'Moderado (ejercicio moderado 3-5 días/semana)'),
        ('active', 'Activo (ejercicio intenso 6-7 días/semana)'),
        ('very_active', 'Muy Activo (ejercicio muy intenso y trabajo físico)')
    ], string="Nivel de Actividad")

    job_description_neat = fields.Text(string="Descripción del Trabajo/Estilo de Vida (para NEAT)")
    instagram_handle = fields.Char(string="Usuario de Instagram")
    
    initial_picture = fields.Image(string="Foto Inicial", max_width=1920, max_height=1920)
    
    # Campos relacionales One2many (se activarán a medida que definamos los otros modelos)
    # fitness_user_program_ids = fields.One2many('fitness.user.program', 'user_id', string="Inscripciones a Programas")
    # fitness_workout_history_ids = fields.One2many('fitness.workout.history', 'user_id', string="Historial de Entrenamientos")
    # fitness_body_measurement_ids = fields.One2many('fitness.body.measurement', 'user_id', string="Mediciones Corporales")
    # fitness_assessment_ids = fields.One2many('fitness.assessment', 'user_id', string="Evaluaciones Físicas")
    fitness_meal_log_ids = fields.One2many('fitness.meal.log', 'user_id', string="Registros de Comidas")
    # fitness_goal_ids = fields.One2many('fitness.goal', 'user_id', string="Metas")
    # fitness_user_achievement_ids = fields.One2many('fitness.user.achievement', 'user_id', string="Logros de Usuario")
    # fitness_user_protocol_ids = fields.One2many('fitness.user.protocol', 'user_id', string="Protocolos de Usuario") 