# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    xaa_aa_sign = fields.Binary(string="Digital Sign")
