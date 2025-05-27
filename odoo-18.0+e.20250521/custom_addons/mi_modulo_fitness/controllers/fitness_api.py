# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

class FitnessAPI(http.Controller):

    @http.route('/api/fitness/check_program_access', type='json', auth='user', methods=['POST'])
    def check_program_access(self, user_id, program_id):
        """
        API endpoint para verificar si un usuario tiene acceso a un programa
        basado en su suscripción activa
        """
        try:
            # Verificar acceso usando el método del modelo
            result = request.env['fitness.user.program'].check_user_program_access(user_id, program_id)
            
            # Obtener información adicional del programa
            program = request.env['fitness.program'].browse(program_id)
            user = request.env['res.partner'].browse(user_id)
            
            # Obtener suscripciones requeridas
            required_subscriptions = program.allowed_subscription_product_ids.mapped('name')
            
            # Obtener suscripciones activas del usuario (Odoo 18)
            active_subscriptions = request.env['sale.order'].search([
                ('partner_id', '=', user_id),
                ('is_subscription', '=', True),
                ('subscription_state', 'in', ['3_progress', '4_paused']),
            ])
            user_subscriptions = active_subscriptions.mapped('plan_id.name')
            
            return {
                'success': True,
                'has_access': result['has_access'],
                'message': result['message'],
                'program_name': program.name,
                'user_name': user.name,
                'required_subscriptions': required_subscriptions,
                'user_subscriptions': user_subscriptions,
                'is_free_program': not bool(required_subscriptions)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'has_access': False
            }

    @http.route('/api/fitness/user_available_programs', type='json', auth='user', methods=['POST'])
    def get_user_available_programs(self, user_id):
        """
        API endpoint para obtener todos los programas disponibles para un usuario
        basado en sus suscripciones activas
        """
        try:
            user = request.env['res.partner'].browse(user_id)
            
            # Obtener suscripciones activas del usuario (Odoo 18)
            active_subscriptions = request.env['sale.order'].search([
                ('partner_id', '=', user_id),
                ('is_subscription', '=', True),
                ('subscription_state', 'in', ['3_progress', '4_paused']),
            ])
            user_subscription_products = active_subscriptions.mapped('order_line.product_template_id')
            
            # Obtener todos los programas activos
            all_programs = request.env['fitness.program'].search([('active', '=', True)])
            
            available_programs = []
            restricted_programs = []
            
            for program in all_programs:
                program_data = {
                    'id': program.id,
                    'name': program.name,
                    'description': program.description,
                    'difficulty': program.difficulty_id.name if program.difficulty_id else '',
                    'category': program.program_category_id.name if program.program_category_id else '',
                    'duration': program.duration_text,
                    'required_subscriptions': program.allowed_subscription_product_ids.mapped('name')
                }
                
                # Si el programa no tiene restricciones, está disponible
                if not program.allowed_subscription_product_ids:
                    program_data['access_type'] = 'free'
                    available_programs.append(program_data)
                else:
                    # Verificar si el usuario tiene acceso
                    has_access = bool(set(user_subscription_products.ids) & set(program.allowed_subscription_product_ids.ids))
                    if has_access:
                        program_data['access_type'] = 'subscription'
                        available_programs.append(program_data)
                    else:
                        program_data['access_type'] = 'restricted'
                        restricted_programs.append(program_data)
            
            return {
                'success': True,
                'user_name': user.name,
                'available_programs': available_programs,
                'restricted_programs': restricted_programs,
                'user_subscriptions': active_subscriptions.mapped('plan_id.name'),
                'total_available': len(available_programs),
                'total_restricted': len(restricted_programs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/api/fitness/subscription_plans', type='json', auth='user', methods=['GET'])
    def get_subscription_plans(self):
        """
        API endpoint para obtener todos los planes de suscripción disponibles
        """
        try:
            # Obtener productos de suscripción y productos fitness gratuitos
            subscription_products = request.env['product.template'].search([
                '|', 
                ('recurring_invoice', '=', True),
                '&', ('recurring_invoice', '=', False), ('name', 'ilike', 'fitness'),
                ('sale_ok', '=', True)
            ])
            
            plans = []
            for product in subscription_products:
                # Contar programas que incluye cada plan
                programs_included = request.env['fitness.program'].search_count([
                    ('allowed_subscription_product_ids', 'in', product.id),
                    ('active', '=', True)
                ])
                
                plans.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.list_price,
                    'description': product.description,
                    'programs_included': programs_included
                })
            
            return {
                'success': True,
                'subscription_plans': plans
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 