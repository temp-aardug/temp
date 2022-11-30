# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _action_open_new_timesheet(self, time_spent):
        '''Override base method to add default description field'''
        return {
            'name': _('Confirm Time Spent'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket.create.timesheet',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                **self.env.context,
                'active_id': self.id,
                'active_model': self._name,
                'default_time_spent': time_spent,
                'default_description': self.name + ' - ' + str(
                    time_spent) +' - ' + self.env.user.name
            }
        }
