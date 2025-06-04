# -*- coding: utf-8 -*-
{
   'name': "HAK Sale Prediction",

    'summary': "Sale Prediction minimun and maximum",

    'description': """
                    The code predicts future product sales based on historical data, updating sale forecasts for short and long-term periods. It also creates reordering rules in Odoo to ensure inventory levels are maintained.
    """,

    'author': "HAK Technologies",
    'website': "https://www.HAKTechnologies.com",
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product','stock'],

    # always loaded
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

}

