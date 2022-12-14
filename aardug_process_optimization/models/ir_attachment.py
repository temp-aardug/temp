# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class Attachments(models.Model):
    _inherit = 'ir.attachment'

    x_aa_po_task_id = fields.Many2one('project.task', string="Task")
    x_aa_po_order_id = fields.Many2one('sale.order', string="Sale Order")
    x_aa_po_lead_id = fields.Many2one('crm.lead', string="Opportunity")
    x_aa_po_ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")
