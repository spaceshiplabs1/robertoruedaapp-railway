# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FitnessFoodItem(models.Model):
    _name = 'fitness.food.item'
    _description = 'Alimento (Biblioteca para Seguimiento Nutricional)'
    _order = 'name'

    name = fields.Char(string="Nombre del Alimento", required=True, index=True)
    serving_size_description = fields.Char(
        string="Descripción de la Porción", 
        required=True,
        help="Ej: 100g, 1 taza (240ml), 1 pieza (50g), 1 scoop (30g)"
    )
    
    # Información nutricional por la porción descrita arriba
    calories_per_serving = fields.Float(string="Calorías (por porción)")
    protein_grams_per_serving = fields.Float(string="Proteínas (g por porción)")
    carbs_grams_per_serving = fields.Float(string="Carbohidratos (g por porción)")
    fat_grams_per_serving = fields.Float(string="Grasas (g por porción)")
    
    notes = fields.Text(string="Notas Adicionales / Marca")
    active = fields.Boolean(string="Activo", default=True, help="Disponible para ser seleccionado.")

    # Podríamos añadir una categoría de alimento si se vuelve necesario
    # food_category_id = fields.Many2one('fitness.food.category', string="Categoría de Alimento")


class FitnessMealLog(models.Model):
    _name = 'fitness.meal.log'
    _description = 'Registro de Comida del Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'user_id, date_time desc'

    name = fields.Char(string="Referencia de Comida", compute='_compute_log_name', store=True, readonly=True)
    
    user_id = fields.Many2one(
        comodel_name='res.partner', 
        string="Usuario", 
        required=True, 
        ondelete='cascade', 
        index=True,
        tracking=True
    )
    date_time = fields.Datetime(
        string="Fecha y Hora", 
        required=True, 
        default=fields.Datetime.now, 
        index=True,
        tracking=True
    )
    meal_type = fields.Selection([
        ('breakfast', 'Desayuno'),
        ('lunch', 'Almuerzo/Comida'),
        ('dinner', 'Cena'),
        ('snack_am', 'Snack (Mañana)'),
        ('snack_pm', 'Snack (Tarde)'),
        ('snack_pre_workout', 'Snack (Pre-Entreno)'),
        ('snack_post_workout', 'Snack (Post-Entreno)'),
        ('other', 'Otro')
    ], string="Tipo de Comida", required=True, tracking=True)
    
    notes = fields.Text(string="Notas sobre la Comida")
    
    meal_line_ids = fields.One2many(
        comodel_name='fitness.meal.line', 
        inverse_name='meal_log_id', 
        string="Alimentos Consumidos",
        copy=True
    )

    # Campos calculados para totales de la comida
    total_calories_meal = fields.Float(string="Total Calorías Comida", compute='_compute_meal_totals', store=True)
    total_protein_meal = fields.Float(string="Total Proteínas Comida (g)", compute='_compute_meal_totals', store=True)
    total_carbs_meal = fields.Float(string="Total Carbohidratos Comida (g)", compute='_compute_meal_totals', store=True)
    total_fat_meal = fields.Float(string="Total Grasas Comida (g)", compute='_compute_meal_totals', store=True)

    @api.depends('user_id.name', 'date_time', 'meal_type')
    def _compute_log_name(self):
        for record in self:
            user_name = record.user_id.name if record.user_id else "N/D"
            date_str = fields.Datetime.context_timestamp(record, record.date_time).strftime('%Y-%m-%d %H:%M') if record.date_time else "N/D"
            meal_type_display = dict(record._fields['meal_type'].selection).get(record.meal_type, '')
            record.name = f"Comida: {user_name} - {meal_type_display} ({date_str})"

    @api.depends('meal_line_ids.calories_line', 'meal_line_ids.protein_line', 'meal_line_ids.carbs_line', 'meal_line_ids.fat_line')
    def _compute_meal_totals(self):
        for log in self:
            log.total_calories_meal = sum(line.calories_line for line in log.meal_line_ids)
            log.total_protein_meal = sum(line.protein_line for line in log.meal_line_ids)
            log.total_carbs_meal = sum(line.carbs_line for line in log.meal_line_ids)
            log.total_fat_meal = sum(line.fat_line for line in log.meal_line_ids)


class FitnessMealLine(models.Model):
    _name = 'fitness.meal.line'
    _description = 'Línea de Alimento en un Registro de Comida'
    _order = 'meal_log_id, sequence, id'

    name = fields.Char(string="Descripción Línea", compute='_compute_line_name', store=True, readonly=True)
    sequence = fields.Integer(default=10)

    meal_log_id = fields.Many2one(
        comodel_name='fitness.meal.log', 
        string="Registro de Comida", 
        required=True, 
        ondelete='cascade', 
        index=True
    )
    food_item_id = fields.Many2one(
        comodel_name='fitness.food.item', 
        string="Alimento", 
        required=True, 
        ondelete='restrict' # No borrar alimento si está en uso
    )
    
    number_of_servings = fields.Float(
        string="Cantidad de Porciones", 
        required=True, 
        default=1.0,
        digits='Product Unit of Measure', # Para precisión decimal
        help="Número de porciones consumidas, según la 'Descripción de la Porción' del alimento."
    )
    
    # Campos calculados para esta línea específica
    calories_line = fields.Float(string="Calorías", compute='_compute_line_nutrients', store=True)
    protein_line = fields.Float(string="Proteínas (g)", compute='_compute_line_nutrients', store=True)
    carbs_line = fields.Float(string="Carbohidratos (g)", compute='_compute_line_nutrients', store=True)
    fat_line = fields.Float(string="Grasas (g)", compute='_compute_line_nutrients', store=True)
    
    notes = fields.Char(string="Notas de la Línea")

    @api.depends('food_item_id.name', 'number_of_servings', 'food_item_id.serving_size_description')
    def _compute_line_name(self):
        for record in self:
            food_name = record.food_item_id.name if record.food_item_id else "N/D"
            serv_desc = record.food_item_id.serving_size_description if record.food_item_id else ""
            record.name = f"{record.number_of_servings} x {food_name} ({serv_desc})"

    @api.depends('food_item_id.calories_per_serving', 'food_item_id.protein_grams_per_serving', 
                 'food_item_id.carbs_grams_per_serving', 'food_item_id.fat_grams_per_serving', 
                 'number_of_servings')
    def _compute_line_nutrients(self):
        for line in self:
            if line.food_item_id and line.number_of_servings > 0:
                line.calories_line = line.number_of_servings * line.food_item_id.calories_per_serving
                line.protein_line = line.number_of_servings * line.food_item_id.protein_grams_per_serving
                line.carbs_line = line.number_of_servings * line.food_item_id.carbs_grams_per_serving
                line.fat_line = line.number_of_servings * line.food_item_id.fat_grams_per_serving
            else:
                line.calories_line = 0
                line.protein_line = 0
                line.carbs_line = 0
                line.fat_line = 0 