# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Kanban Automation CRM',
    'category': 'CRM',
    'description': """
        To support CRM Opportunity kanban.
        1) add customer in follower list in opportunity.
        2) user can set server action and custom action on crm stage configuration.
        3) server action is very helpfull to do any action on opportunity like automatically stage.
        4) custom action is to set activity on opportunity automatically.
    """,
    'version': '16.0.0.1',
    'depends':['crm'],
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'data' : [
        'security/ir.model.access.csv',
        'data/crm_action_rule_data.xml',
        'views/crm_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            '/kanban_automation_crm/static/src/scss/web_kanban_custom.scss'
        ],
    },
    'license': 'LGPL-3',
}
