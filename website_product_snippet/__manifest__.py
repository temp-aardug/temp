# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "Website Product Template",
    'version': '15.0.0.1',
    'category': 'Website',
    'summary': '',
    'description': """
                1. Add some fields in product template and add page "website" in product template view.
                2. Add snippet in website.
                """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['website_sale'],
    'data': [
        'views/product_template_view.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_product_snippet/static/src/js/snippet_data.js'
        ],
    },
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'auto_install': False,
}
