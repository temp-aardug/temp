# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models,fields


class HelpdeskTicketCreateTimesheet(models.TransientModel):
    _inherit = 'helpdesk.ticket.create.timesheet'

    xaa_aa_long_desc_id = fields.Many2one('helpdesk.description', string='Long Descriptions')
    xaa_aa_long_desc = fields.Char(string='Long Description')

    def action_generate_timesheet(self):
        '''Overwrite method to add long description'''
        values = {
            'name': self.description,
            'project_id': self.ticket_id.project_id.id,
            'date': fields.Datetime.now(),
            'user_id': self.env.uid,
            'unit_amount': self.time_spent,
            'long_description': self.xaa_aa_long_desc_id.xaa_aa_name \
            if self.xaa_aa_long_desc_id.xaa_aa_name else self.xaa_aa_long_desc,
        }
        timesheet = self.env['account.analytic.line'].create(values)
        self.ticket_id.write({
            'timer_start': False,
            'timer_pause': False,
            'timesheet_ids': [(4, timesheet.id, None)]
        })
        self.ticket_id.user_timer_id.unlink()
        return timesheet
