# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessDifficulty(models.Model):
    _name = 'fitness.difficulty'
    _description = 'Niveles de Dificultad'
    _order = 'sequence, name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    sequence = fields.Integer(string="Secuencia", default=10)
    color = fields.Integer(string="Color", help="Color para la interfaz")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del nivel de dificultad debe ser único.')
    ]


class FitnessProgramCategory(models.Model):
    _name = 'fitness.program.category'
    _description = 'Categorías de Programas de Entrenamiento'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    color = fields.Integer(string="Color", help="Color para la interfaz")
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre de la categoría debe ser único.')
    ]


class FitnessProgramType(models.Model):
    _name = 'fitness.program.type'
    _description = 'Tipos de Programas de Entrenamiento'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del tipo debe ser único.')
    ]


class FitnessEquipment(models.Model):
    _name = 'fitness.equipment'
    _description = 'Equipos de Entrenamiento'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    image = fields.Image(string="Imagen", max_width=1024, max_height=1024)
    active = fields.Boolean(string="Activo", default=True)
    
    # Campos adicionales útiles
    brand = fields.Char(string="Marca")
    model = fields.Char(string="Modelo")
    purchase_date = fields.Date(string="Fecha de Compra")
    cost = fields.Float(string="Costo")
    location = fields.Char(string="Ubicación")
    maintenance_notes = fields.Text(string="Notas de Mantenimiento")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del equipo debe ser único.')
    ]


class FitnessMuscleGroup(models.Model):
    _name = 'fitness.muscle.group'
    _description = 'Grupos Musculares'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    anatomical_region = fields.Selection([
        ('upper_body', 'Tren Superior'),
        ('lower_body', 'Tren Inferior'),
        ('core', 'Core/Abdomen'),
        ('full_body', 'Cuerpo Completo')
    ], string="Región Anatómica")
    image = fields.Image(string="Imagen Anatómica", max_width=1024, max_height=1024)
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del grupo muscular debe ser único.')
    ]


class FitnessAssessmentType(models.Model):
    _name = 'fitness.assessment.type'
    _description = 'Tipos de Evaluaciones Físicas'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    measurement_unit = fields.Char(string="Unidad de Medida", help="Ej: kg, cm, segundos, repeticiones")
    instructions = fields.Text(string="Instrucciones de Evaluación")
    assessment_category = fields.Selection([
        ('strength', 'Fuerza'),
        ('endurance', 'Resistencia'),
        ('flexibility', 'Flexibilidad'),
        ('balance', 'Equilibrio'),
        ('power', 'Potencia'),
        ('speed', 'Velocidad'),
        ('agility', 'Agilidad')
    ], string="Categoría de Evaluación")
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del tipo de evaluación debe ser único.')
    ]


class FitnessGoalType(models.Model):
    _name = 'fitness.goal.type'
    _description = 'Tipos de Metas de Fitness'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    measurement_type = fields.Selection([
        ('weight', 'Peso'),
        ('percentage', 'Porcentaje'),
        ('time', 'Tiempo'),
        ('repetitions', 'Repeticiones'),
        ('distance', 'Distancia'),
        ('frequency', 'Frecuencia'),
        ('qualitative', 'Cualitativo')
    ], string="Tipo de Medición")
    default_target_period_days = fields.Integer(string="Período Objetivo por Defecto (días)", default=30)
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del tipo de meta debe ser único.')
    ]


class FitnessWorkoutType(models.Model):
    _name = 'fitness.workout.type'
    _description = 'Tipos de Entrenamiento'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    workout_style = fields.Selection([
        ('strength', 'Fuerza'),
        ('cardio', 'Cardiovascular'),
        ('hiit', 'HIIT'),
        ('flexibility', 'Flexibilidad'),
        ('circuit', 'Circuito'),
        ('functional', 'Funcional'),
        ('sport_specific', 'Específico de Deporte')
    ], string="Estilo de Entrenamiento")
    typical_duration_minutes = fields.Integer(string="Duración Típica (minutos)")
    intensity_level = fields.Selection([
        ('low', 'Baja'),
        ('moderate', 'Moderada'),
        ('high', 'Alta'),
        ('variable', 'Variable')
    ], string="Nivel de Intensidad")
    active = fields.Boolean(string="Activo", default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El nombre del tipo de entrenamiento debe ser único.')
    ] 