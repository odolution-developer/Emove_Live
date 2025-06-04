{
    'name': 'Products Labels Barcode ',
    'summary': 'Products Labels Barcode ',
    'version': '17.2',
    'price': 0,
    "author" : "Osama Ramadan",
    'sequence': 1,
    'license': 'OPL-1',
    'category': 'product',
    	"images": [
		"static/description/thumbnail.png"
	],
    'depends': [
        'product', 'purchase'
    ],
    'data': [
        'views/views.xml',
        'report/product_product_templates.xml',
    ],
    'demo': [
    ],
    "external_dependencies": {"python": ["deep-translator"]},
    'installable': True,
    'auto_install': False,
    'application': False,
}
