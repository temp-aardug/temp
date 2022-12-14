# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    x_aa_caret_website_url = fields.Char(
        string='Caret website url',
        config_parameter='aardug_caret_pms_sync.x_aa_caret_website_url')
    x_aa_caret_token = fields.Char(
        string='Caret token',
        config_parameter='aardug_caret_pms_sync.x_aa_caret_token')
