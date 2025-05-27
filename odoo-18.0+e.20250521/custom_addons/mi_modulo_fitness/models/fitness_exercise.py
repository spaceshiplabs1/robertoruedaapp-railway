# -*- coding: utf-8 -*-

from odoo import models, fields

class FitnessExercise(models.Model):
    _name = 'fitness.exercise'
    _description = 'Ejercicio Individual (Biblioteca de Movimientos)'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para historial y actividades
    _order = 'name' # Ordenar alfabéticamente por nombre por defecto

    name = fields.Char(string="Nombre del Ejercicio", required=True, tracking=True, index=True)
    description = fields.Text(string="Descripción/Instrucciones del Ejercicio", translate=True)

    primary_muscle_group_id = fields.Many2one(
        comodel_name='fitness.muscle.group',
        string="Grupo Muscular Primario",
        tracking=True,
        ondelete='restrict' # Evitar borrar un grupo muscular si está en uso
    )
    secondary_muscle_group_ids = fields.Many2many(
        comodel_name='fitness.muscle.group',
        relation='fitness_exercise_secondary_muscle_rel',
        column1='exercise_id',
        column2='muscle_group_id',
        string="Grupos Musculares Secundarios"
    )

    required_equipment_ids = fields.Many2many(
        comodel_name='fitness.equipment',
        relation='fitness_exercise_equipment_rel',
        column1='exercise_id',
        column2='equipment_id',
        string="Equipamiento Requerido"
    )

    difficulty_id = fields.Many2one(
        comodel_name='fitness.difficulty',
        string="Nivel de Dificultad",
        tracking=True,
        ondelete='restrict' # Evitar borrar una dificultad si está en uso
    )

    # Multimedia para demostración
    image_1920 = fields.Image(string="Imagen Demostrativa", max_width=1920, max_height=1920)
    video_url = fields.Char(
        string="URL del Video Demostrativo",
        help="Enlace a un video externo (ej. YouTube, Vimeo) que muestre cómo realizar el ejercicio."
    )
    
    internal_notes = fields.Text(
        string="Notas Internas (para Entrenadores)",
        help="Observaciones o puntos clave sobre el ejercicio para uso interno del entrenador."
    )

    active = fields.Boolean(
        string="Activo", 
        default=True, 
        help="Desmarcar para archivar el ejercicio y que no esté disponible para ser añadido a nuevos entrenamientos."
    )

    # Podríamos añadir un constraint para asegurar que el nombre del ejercicio sea único
    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "El nombre del ejercicio debe ser único.")
    # ] 