# -*- coding: utf-8 -*-
{
    'name' : 'Import Woo Feed',
    'version' : '1.7',
    'summary': 'Import Woo Feed',
    'description': """Import Woo Feedt""",
    'author' : "HAK Technology",
    'category': 'inventory',
    'website': '',
    'depends' : ['stock','purchase','product'],
    'data': [
        # 'security/ir.model.access.csv',
        #  'data/data.xml',
         'model/views.xml'
            ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
