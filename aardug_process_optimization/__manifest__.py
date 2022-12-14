# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Porject Optimization',
    'category': 'project',
    'summary': 'Porject Optimization',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'version': '16.0.1.0',
    'description': '''
                * Added Custom Fields in Contact, Task, and Ticket
                * Create task from ticket 
                * Added smart button in task for linking ticket
                * Added alias for Quotation,Crm,Ticket and Task
                * Add field 'Customer Company' and the info in tab
                  'Odoo Klantinfo' fetched from this field.
                * Add Ticket number in 'Ticket Nr' field on task.
                * Add Attachment filed on task after description field
                * Add button on task 'Email to Caret' for send mail
                  with attachment to caret.
     ''',
    'depends': ['project', 'helpdesk_timesheet',
                'helpdesk_sale', 'sale_management', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/opportunity_sequence.xml',
        'views/res_partner_view.xml',
        'views/helpdesk_ticket_view.xml',
        'views/project_task_view.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
