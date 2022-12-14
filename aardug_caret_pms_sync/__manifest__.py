# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Aardug Caret PMS sync',
    'version': '16.0.1.0',
    'category': 'CRM',
    'sequence': 1,
    'summary': 'Create Task on Linked Server using "aardug pms task" '
               'button On Project Task',
    'description':
        """
        This module make connection between aardug and caret site and also 
        send some data to caret pms task.
        1. Add caret URL and token in general setting, token must be same of 
        caret site.
        2. Add Create aardug pms task button on task for create task on 
        caret side.
        3. display success message after create task, also display proper 
        error message.
        """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['project', 'aardug_process_optimization'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/task_create_view.xml',
        'views/res_config_settings_views.xml',
        'views/task_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'license': 'LGPL-3',
}
