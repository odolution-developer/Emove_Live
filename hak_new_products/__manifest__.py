# -*- coding: utf-8 -*-
{
    'name': "Optional Product",

    'summary': "Optional Products",

    'description': """
        Optional Products
    """,

    'author': "HAK Technologies",
    'website': "https://www.HAKTechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}

