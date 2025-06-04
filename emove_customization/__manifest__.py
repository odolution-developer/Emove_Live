# -*- coding: utf-8 -*-
{
    'name': "Emove Customization",

    'summary': "This code extends `stock.warehouse.orderpoint` to add related product fields"
               " and sales tracking for the last and next 90 days in a customized view.",

    'description': """
            This code customizes `stock.warehouse.orderpoint` by adding related product details, such as SKU, EAN, 
            HS code, barcode, weight, image, category, cost, and sale price. It also introduces fields for tracking 
            sales over the last and forecasting for the next 90 days. 
            These fields are displayed in a modified tree view to enhance inventory tracking and planning.
    """,

    'author': "HAK Technologies",
    'website': "https://www.HAKTechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Uncategorized',
    'version': '0.9',

    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock', 'purchase',  'stock_delivery'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_order_inh.xml',
        'views/product_product_inh.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'purchase/static/src/views/*.js',
            'emove_customization/static/src/views/purchaseDashboard.xml',
        ],

    },
}

