# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Locaties',
    'version': '16.0.0.1',
    'summary': '',
    'description': """ 
        Module to add the functionality of the locaties as a different model also it's 
        combine the phase of maintenance and helpdesk tickets.
        """,
    'category': 'location',
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'depends': ['helpdesk', 'maintenance', 'contacts', 'stock', 'crm', 'web_map'],
    'data': [
        'security/ir.model.access.csv',
        'data/locatie_stage_data.xml',
        'views/locatie_view.xml',
        'views/locatie_config_view.xml',
        'views/res_partner_view.xml',
        'views/crm_lead.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
