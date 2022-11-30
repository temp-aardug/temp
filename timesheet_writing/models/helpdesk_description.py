# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models,fields


class HelpdeskDescription(models.Model):
    _name = 'helpdesk.description'
    _rec_name = 'xaa_aa_name'
    _description = 'Helpdesk Description'

    xaa_aa_name = fields.Char(string='Name')
