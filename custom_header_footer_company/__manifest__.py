# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Custom Header Footer Based on Company',
    'version': '16.0.0',
    'category': 'Reports',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'license': 'LGPL-3',
    'support': 'arosman@aardug.nl',
    'description': """
        1) Take Header and Footer image from company and print in reports
    """,
    'depends': ['custom_header_footer','quote_print'],
    'data': ['views/res_company.xml',
             'report/external_header_footer.xml'],
    'installable': True,
    'application': False,
}
