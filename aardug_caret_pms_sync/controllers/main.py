# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CustomerPortal(http.Controller):

    @http.route(['/pms_task_update'], type='http', auth="public",
                website=False, csrf=False)
    def pms_task_update(self, **kw):
        """ Fetch data from linked server and update on Project Task,
                or Give Proper Error Msg/Response"""
        Task = request.env['project.task'].sudo()
        x_aa_caret_token = request.env['ir.config_parameter'].\
            sudo().get_param('aardug_caret_pms_sync.x_aa_caret_token')
        if x_aa_caret_token and x_aa_caret_token == kw.get(
                'aardug_token', ''):
            task_id = Task.search(
                [('x_aa_po_code', '=', kw.get('task_code', ''))],
                limit=1)
            assign_to = request.env['res.partner'].sudo().search(
                [('email', '=ilike', kw.get('assign_to', ''))], limit=1)
            if task_id:
                task_id.write({
                    'x_aa_po_job_nr_caret':
                        kw.get('x_aa_po_job_nr_caret', ''),
                    'x_aa_po_expected_start_date': kw.get(
                        'x_aa_po_expected_start_date', ''),
                    'x_aa_po_expected_delivery_date': kw.get(
                        'x_aa_po_expected_delivery_date', ''),
                    'x_aa_po_real_start_date': kw.get(
                        'x_aa_po_real_start_date', ''),
                    'x_aa_po_real_delivery_date': kw.get(
                        'x_aa_po_real_delivery_date', ''),
                    'x_aa_po_note': kw.get('x_aa_po_note', '') or '',
                    'x_aa_po_team_member_ids': assign_to and (
                        4, assign_to.id) or False,
                    })
                return request.make_response(json.dumps(
                    {'status': 'Finished'}))
            else:
                _logger.error("Task not found: <%s>", str(kw.get(
                    'task_code', '')))
                return request.make_response(json.dumps({'status': 'Error'}))
        else:
            _logger.error("Token not found.")
            return request.make_response(json.dumps({'status': 'Error'}))
