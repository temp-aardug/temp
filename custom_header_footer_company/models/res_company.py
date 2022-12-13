# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class CompanyInherit(models.Model):
    _inherit = "res.company"

    xaa_aa_header_image = fields.Binary("Header Image")
    xaa_aa_footer_image = fields.Binary("Footer Image")
    xaa_aa_file_name_footer = fields.Char('Footer file Name')
    xaa_aa_file_name_header = fields.Char('Header file Name')
