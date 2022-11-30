# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Timesheet writing',
    'version': '16.0.1.1',
    'summary': 'timesheet writing in v16',
    'category': '',
    'description': """ timesheet writing in v16
    * Change some base field lable name.
    * Add long description and upload image on timsheet writing.
    * Add timeshet using website my timesheet menu.
    * Customise base timesheet report.
    * Compute total amount of time based on product which set on project.
    * Add fields on user for timesheet access based on users.
    """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['odoo_mobile_timesheet', 'project', 'analytic', 'account', 
    'hr_timesheet','helpdesk_timesheet', 'website' ,'portal', 'sale_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/analytic_account_views.xml',
        'views/project_task.xml',
        'views/website_portal_templates.xml',
        'views/res_users_view.xml',
        'views/timesheet_work_type_view.xml',
        'views/project_view.xml',
        'report/timesheet_inherit.xml',
        'views/account_analytic_line_view.xml',
        'wizard/helpdesk_ticket_create_timesheet_view.xml',
        'views/helpdesk_ticket_view.xml',
        'views/helpdesk_description_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/timesheet_writing/static/src/js/custom_timesheet.js',
            '/timesheet_writing/static/src/js/image_upload.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
