# -*- coding: utf-8 -*-
{
    'name': "Emove Reporting",

    'summary': "Generates customizable delivery slip and invoice reports in Spanish.",

    'description': """
        The Emove Reporting module allows for the creation of fully customizable delivery slip and invoice reports in Spanish.
        It offers users the ability to modify layouts, headers, and fields easily, ensuring compliance with local requirements.
        The module features a user-friendly interface for quick report generation,
        making it an essential tool for businesses looking to enhance their documentation and present professional reports to clients.
    """,

    'author': "HAK Technologies",
    'website': "https://www.HAKTechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Uncategorized',
    'version': '0.4',

    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/delivery_slip.xml',
        'report/invoice_report.xml',
        # 'report/report_picking.xml',
        'report/shipping_label.xml',
        'report/cluster_picking.xml',
        'views/stock_view_inh.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

