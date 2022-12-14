# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_aa_po_sale_alias = fields.Many2one(
        'mail.alias', 'Alias', readonly=True)
    xaa_aa_attachment_ids = fields.One2many(
        'ir.attachment', 'x_aa_po_order_id',
        string='Attachments')

    @api.model
    def create(self, vals):
        """Create mail alias from so"""
        res = super(SaleOrder, self).create(vals)
        ir_model = self.env['ir.model'].search(
            [('model', '=', 'sale.order')])
        res.x_aa_po_sale_alias = self.env['mail.alias'].sudo().create(
            {'alias_name': res.name,
             'alias_model_id': ir_model.id,
             'alias_defaults': {'x_aa_po_order_id': res.id}, }).id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Checked Documents are already there or not and
        added in message custom value"""
        if custom_values is None:
            custom_values = {}
        order = custom_values.get('x_aa_po_order_id')
        return order and self.env['sale.order'].browse(
            order) or super(SaleOrder, self).message_new(
            msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype_id=None, **kwargs):
        """ Checked if message type is email then set
        mt_comments and send that."""
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype_id = self.env.ref('mail.mt_comment').id
        return super(SaleOrder, self). \
            message_post(subtype_id=subtype_id, **kwargs)
