# -*- coding: utf-8 -*-
{
    'name': "Mi Módulo de Fitness",
    'version': '1.0',
    'summary': "Gestión integral para negocios de fitness y entrenamiento personalizado.",
    'description': """
        Módulo para gestionar programas de entrenamiento, seguimiento de clientes,
        historial de ejercicios, mediciones corporales, nutrición y más.
    """,
    'author': "Tu Nombre o Nombre de tu Empresa",
    'category': 'Services/Fitness',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'product', 'sale_subscription'],
    'data': [
        'security/ir.model.access.csv',
        'data/fitness_seed_data_fase1.xml',
        'data/fitness_seed_data_fase2.xml',
        'data/fitness_seed_data_fase3.xml',
        'data/fitness_seed_data_fase4.xml',
        'data/fitness_seed_data_fase5.xml',
        'data/fitness_seed_data_fase6.xml',
        'data/fitness_seed_data_fase7.xml',
        'data/fitness_seed_data_fase8.xml',
        'data/fitness_seed_data_fase9.xml',
        'data/fitness_seed_data_fase10.xml',
        'data/fitness_seed_data_fase11_subscriptions.xml',
        'data/odoo_standard_modules_seed_data.xml',
        'views/fitness_program_views.xml',
        'views/fitness_exercise_views.xml',
        'views/fitness_catalog_views.xml',
        'views/fitness_tracking_views.xml',
        'views/fitness_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mi_modulo_fitness/static/src/css/fitness_responsive_clean.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
} 