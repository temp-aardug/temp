# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import json
import urllib.parse
import urllib.request
from odoo import fields, models, _
from odoo.exceptions import UserError


class Task(models.Model):
    _inherit = 'project.task'

    x_aa_task_create_for_caret = fields.Boolean(
        string='task created for caret')

    def create_caret_pms_task(self):
        """ Match caret token and fetch aardug projects for 'project
        selection' field or Raise User error"""

        caret_url = self.env['ir.config_parameter'].sudo().get_param(
            'aardug_caret_pms_sync.x_aa_caret_website_url')
        caret_token = self.env['ir.config_parameter'].sudo().get_param(
            'aardug_caret_pms_sync.x_aa_caret_token')
        if not caret_token:
            raise UserError('Add caret token in general settings')
        if caret_url:
            req = urllib.request.Request(caret_url + '/get_pms_projects',
                                         urllib.parse.urlencode(
                                             {'caret_token': caret_token}
                                         ).encode('ascii'))
            data = json.loads(urllib.request.urlopen(req).read())
            if data.get('status', '') == 'Error':
                raise UserError('Token not matched!')
            else:
                return {
                    'name': _('Caret task create'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'caret.task.create',
                    'view_id': self.env.ref(
                        'aardug_caret_pms_sync.caret_task_create_view_form').id,
                    'target': 'new',
                    'context': {
                        'default_x_aa_task_id': self.id,
                        'default_x_aa_project_id': data.get('projects', ''), },
                }
        else:
            raise UserError('Add caret website url in general settings')
