{
    'name': 'Emove Stages',
    'version': '1.0',
    'category': 'Customizations',
    'author': 'Pawan Kumar',
    "sequence": -101,
    'depends': ['stock', 'sale_stock', 'sale', 'stock_delivery', 'stock_barcode_picking_batch', 'stock_picking_batch'],
    'summary': '',
    'description': '',
    'data': [
        'security/ir.model.access.csv',
        'views/picking_stages_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_picking_batch_view.xml',
        'views/stock_quant_package_view.xml'

        
    ],

    'assets': {
        'web.assets_backend': [
            'ol_stage_ext/static/src/**/*.js',
            'ol_stage_ext/static/src/components/inherit_line.xml',
            'ol_stage_ext/static/src/components/inherit_main.xml',
            # 'ol_stage_ext/static/src/**/inherit_line.xml',
            # 'ol_stage_ext/static/src/**/inherit_main.xml',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
