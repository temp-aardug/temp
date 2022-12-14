# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    x_aa_po_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    x_aa_po_attachment_ids = fields.One2many('ir.attachment',
                                             'x_aa_po_lead_id',
                                             string='Attachments')
    xaa_aa_code = fields.Char(string='Opportunity Number', required=False,
                              default="/", readonly=True)

    _sql_constraints = [
        ('opportunity_unique_code', 'UNIQUE (xaa_aa_code)',
         _('The code must be unique!')),
    ]

    def copy(self, default=None):
        """ Create Sequence while lead/opportunity duplicate"""
        if default is None:
            default = {}
        default['xaa_aa_po_code'] = self.env['ir.sequence']. \
            next_by_code('crm.lead')
        return super(Lead, self).copy(default)

    @api.model
    def create(self, vals):
        """ Create Sequence while lead/opportunity
        create and Also Create Mail Alias"""
        if vals.get('xaa_aa_code', '/') == '/':
            vals['xaa_aa_code'] = self.env['ir.sequence']. \
                next_by_code('crm.lead')
        res = super(Lead, self).create(vals)
        res.x_aa_po_alias = self.env['mail.alias'].sudo().create({
            'alias_name': res.xaa_aa_code,
            'alias_model_id': self.env['ir.model'].search(
                [('model', '=', 'crm.lead')]).id,
            'alias_defaults': {'x_aa_po_lead_id': res.id},
            'alias_user_id': res.user_id.id
        }).id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Checked Documents are already there or not
        and added in message custom value"""
        if custom_values is None:
            custom_values = {}
        lead = custom_values.get('x_aa_po_lead_id', None)
        return lead and self.browse(lead) or super(
            Lead, self).message_new(
            msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype_id=None, **kwargs):
        """ Checked if message type is email with
        opportunity then set  mt_comments and send that."""
        self.ensure_one()
        if kwargs.get('message_type') == 'email' \
                and self.type == 'opportunity':
            subtype_id = self.env.ref('mail.mt_comment').id
        return super(Lead, self).message_post(
            subtype_id=subtype_id, **kwargs)
