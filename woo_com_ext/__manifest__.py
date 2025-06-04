# -*- coding: utf-8 -*-
{
    'name': "Woo Commerce Extension",

    'summary': "This code customizes WooCommerce data queue models in Odoo to add automated processing after record creation.",

    'description': """
        Order Processing: Automatically processes order queue lines and imports stock upon record creation in woo.order.data.queue.line.ept.
        Product Sync: Ensures WooCommerce product data synchronization when a product queue line is created in woo.product.data.queue.line.ept.
        Customer Import: Converts customer data from WooCommerce to Odoo for woo.customer.data.queue.line.ept.
        Stock Export: Automates stock export queue processing for woo.export.stock.queue.line.ept.
    """,

    'author': "HAK Technologies",
    'website': "https://www.HAKTechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Uncategorized',
    'version': '0.5',
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'woo_commerce_ept'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}

