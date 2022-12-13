# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api


class ProductSetLines(models.Model):
    _inherit = "product.set.line"

    product_id = fields.Many2one(comodel_name="product.product",
                                 domain=[("sale_ok", "=", True)],
                                 string="Product", required=False)
    name = fields.Text(string="Description")
    display_type = fields.Selection([('line_section', 'Section'),
                                     ('line_note', 'Note')], default=False,
                                    help="Technical field for UX purpose.")
    x_aa_ec_fixed = fields.Boolean(string="Fixed", default=False)

    @api.onchange('product_id')
    def _set_description(self):
        """ set description on product onchange """
        if not self.product_id:
            return
        self.name = self.product_id.display_name and \
                    self.product_id.display_name or ""

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ return missing required fields if it not their."""
        res = {}
        onchange_fields = ['name', 'quantity', 'discount']
        if values.get('product_set_id') and values.get('product_id') and any(
                field_in not in values for field_in in onchange_fields):
            line = self.new(values)
            # This method is not available need to check for that.
            # line.product_id_change()
            for field in onchange_fields:
                if field not in values:
                    res[field] = line._fields[field].convert_to_write(
                        line[field], line)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        '''Set product and quantity are False, when get display type False
        or Prepare missing fields and create lines.'''
        for values in vals_list:
            if values.get('display_type',
                          self.default_get(['display_type'])['display_type']):
                values.update(product_id=False, quantity=0)
            else:
                values.update(self._prepare_add_missing_fields(values))
        return super().create(vals_list)

    def prepare_sale_order_line_values(self, order, quantity, max_sequence):
        '''Update display type,sequence and quantity, in this line if you
               use 'fixed' then this take quantity from line or
               multiply with wizard quantity'''
        res = super(ProductSetLines, self).prepare_sale_order_line_values(
            order, quantity, max_sequence)
        self.display_type and res.update({'display_type': self.display_type,
                                          'name': self.name})
        res.update({
            'product_uom_qty': self.x_aa_ec_fixed and self.quantity or
                               (self.quantity * quantity),
            'sequence': max_sequence + 1
        })
        return res
