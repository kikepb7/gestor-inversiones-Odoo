# -*- coding: utf-8 -*-
{
    'name': "Investments",

    'summary': """
        Empresa de inversiones para rentabilizar tus ahorros""",

    'description': """
        Empresa de inversiones
    """,

    'author': "Enrique Palma",
    'website': "https://www.investment.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inversiones',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/investment.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml'
    ],
    'application': True,
    'sequence': 1
}
