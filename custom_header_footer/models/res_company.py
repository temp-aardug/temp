# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class CompanyInherit(models.Model):
    _inherit = "res.company"

    xaa_aa_for_all_report = fields.Boolean("Use images for all report")

    @api.onchange('xaa_aa_for_all_report')
    def onchange_for_all_report(self):
        """When the Boolean Field Is Checked and if Image Set in the Companies Logo,
        The Image Will be used as Header and Footer for the Reports Generated."""

        if self.xaa_aa_for_all_report == True:
            custom_paper_format = self.env.ref(
                'custom_header_footer.paperformat_custom_header_footer_update')
            self.paperformat_id = custom_paper_format and custom_paper_format.id
        else:
            paperformat_us = self.env.ref('base.paperformat_us', False)
            if paperformat_us and paperformat_us.id or False:
                self.paperformat_id = paperformat_us and paperformat_us.id or False
