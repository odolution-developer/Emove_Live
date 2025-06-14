{
    'name': 'Odoo WooCommerce Connector',
    'version': '17.0.2.7',
    'category': 'eCommerce',
    'license': 'OPL-1',
    'summary': 'Odoo Woocommerce Connector helps you automate your vital business processes at Odoo by enabling bi-directional data exchange between WooCommerce & Odoo.Apart from Odoo Woocommerce Connector, we do have other ecommerce solutions or applications such as Magento connector, Shopify connector, and also we have solutions for Marketplace Integration such as Odoo Amazon connector, Odoo eBay Connector, Odoo Walmart Connector, Odoo Bol.com Connector.Aside from ecommerce integration and ecommerce marketplace integration, we also provide solutions for various operations, such as shipping, logistics, shipping labels and shipping carrier management with our shipping integration, known as the Shipstation connector.For the customers who are into Dropship business, we do provide EDI Integration that can help them manage their Dropshipping business with our Dropshipping integration or Dropshipper integration It is listed as Dropshipping EDI integration and Dropshipper EDI integration.Emipro applications can be searched with different keywords like Amazon integration, Shopify integration, Woocommerce integration, Magento integration, Amazon vendor center module, Amazon seller center module, Inter company transfer, Ebay integration, Bol.com integration, inventory management, warehouse transfer module, dropship and dropshipper integration and other Odoo integration application or module,',

    'author': 'Emipro Technologies Pvt. Ltd.',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',

    'depends': ['common_connector_library'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'data/ir_sequence.xml',
        'data/ir_cron_data.xml',
        'data/ir_attachment_data.xml',
        'data/import_order_status_ept.xml',
        'wizard/manual_queue_process_ept.xml',
        'wizard/cron_configuration_ept.xml',
        'views/instance_main_menu_view.xml',
        'wizard/process_import_export_view.xml',
        'views/product_image_ept.xml',
        'views/product_template_view.xml',
        'views/sale_workflow_config.xml',
        'wizard/res_config_view.xml',
        'views/product_data_queue_ept_view.xml',
        'views/product_data_queue_line_ept_view.xml',
        'views/product_variant_view.xml',
        'views/tags_ept.xml',
        'views/product_attribute_view.xml',
        'views/product_attribute_term_view.xml',
        'views/product_category_view.xml',
        'views/customer_data_queue_ept.xml',
        'views/customer_data_queue_line_ept.xml',
        'views/order_data_queue_ept.xml',
        'views/order_data_queue_line_ept.xml',
        'views/webhook_ept.xml',
        'views/common_log_lines_ept.xml',
        'views/woo_instances_onboarding_panel_view.xml',
        'views/sale_order.xml',
        'views/stock_picking_view.xml',
        'views/res_partner.xml',
        'views/payment_gateway.xml',
        'views/account_move_view.xml',
        'views/instance_view.xml',
        'wizard/cancel_refund_order_wizard.xml',
        'wizard/financial_status_onboarding_view.xml',
        'wizard/basic_configuration_onboarding.xml',
        'wizard/woo_onboarding_confirmation_ept.xml',
        'views/coupons_ept.xml',
        'views/coupon_data_queue_ept.xml',
        'views/coupon_data_queue_line_ept.xml',
        'views/delivery_carrier_view.xml',
        'views/shipping_method.xml',
        'views/export_stock_queue_ept.xml',
        'views/export_stock_queue_line_ept.xml',
        'wizard/prepare_product_for_export.xml',
        'report/sale_report.xml',
        'wizard/instance_configuration_wizard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'woo_commerce_ept/static/src/js/woo_button_collapse.js',
            'woo_commerce_ept/static/src/css/woo_base.css',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'active': False,
    'images': ['static/description/woocommerce-odoo-cover_17.gif'],
    'live_test_url': 'https://www.emiprotechnologies.com/r/IGM',
    'price': 349.00,
    'currency': 'EUR',
    # cloc settings
    'cloc_exclude': ['woocommerce/**/*',
                     'wordpress_xmlrpc/**/*',
                     '**/*.xml',
                     "wizard/**/*",
                     "models/**/*",
                     "data/**/*",
                     "report/**/*",
                     "security/**/*",
                     "static/**/*",
                     "view/**/*",
                     "wizard_views/**/*",
                     "__pycache__/**/*",
                     ],

}
