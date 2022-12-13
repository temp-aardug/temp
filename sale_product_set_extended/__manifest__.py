# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    "name": "Sale Product Set Extended",
    "summary": "Extend sale product set module functionality",
    "description": '''Extend sale product set module functionality for
                    1. Discount
                    2. Fixed (Quantity).
                    3. Add section and note widget in product set lines.
                    ''',
    "version": "16.0.0.1",
    "category": "Custom",
    "license": "LGPL-3",
    "website": "http://www.aardug.nl/",
    "author": "Aardug, Arjan Rosman",
    'support': 'arosman@aardug.nl',
    "depends": ['sale_product_set'],
    "data": [
        "views/product_set_view.xml",
    ],
    "application": False,
    "installable": True,
}
