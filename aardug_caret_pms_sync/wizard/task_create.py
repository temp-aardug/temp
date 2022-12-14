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
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CaretTaskCreate(models.TransientModel):
    _name = 'caret.task.create'
    _description = "Caret task create"
    _rec_name = 'x_aa_task_id'

    x_aa_project_id = fields.Selection('_get_selection',
                                       string="Caret Project",
                                       store=True)
    x_aa_task_id = fields.Many2one('project.task')

    @api.model
    def _get_selection(self):
        """ dynamically get all selection field options"""
        if self.env.context.get('default_x_aa_project_id'):
            return [[project, project] for project in self.env.context.get(
                'default_x_aa_project_id')]

    def action_create(self):
        """ Fetch caret website url and token and create task on linked
        server, success message after create task."""

        caret_url = self.env['ir.config_parameter'].sudo().get_param(
            'aardug_caret_pms_sync.x_aa_caret_website_url')
        caret_token = self.env['ir.config_parameter'].sudo().get_param(
            'aardug_caret_pms_sync.x_aa_caret_token')
        if caret_url:
            task_id = self.x_aa_task_id
            description = \
                task_id.description or ('' + (
                        self.x_aa_project_id
                        and ' Project: '
                        + self.x_aa_project_id or ''
                ) + (
                    task_id.x_aa_po_odoo_version
                    and ' Odoo version: '
                    + task_id.x_aa_po_odoo_version
                    or '') + (
                    task_id.user_ids and ', '.join(
                [user.name for user in task_id.user_ids]) or '')
                                        )
            vals = {
                'name': task_id.name,
                'description': description,
                'aardug_task_code': task_id.x_aa_po_code,
                'project': self.x_aa_project_id,
                'caret_token': caret_token or '',
            }
            req = urllib.request.Request(
                caret_url + '/pms_task_created', urllib.parse.urlencode(
                    vals).encode('ascii'))
            if json.loads(urllib.request.urlopen(req).read()).get(
                    'status', '') == 'Error':
                raise UserError('Something is wrong, Task is not created!')
            task_id.x_aa_task_create_for_caret = True
            message_id = self.env['message.wizard'].create(
                {'x_aa_message': _("Task is successfully created")})
            return {
                'name': _('Successfull'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }
