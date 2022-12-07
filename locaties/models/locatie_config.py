# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class LocatieStage(models.Model):
    _name = 'locatie.stage'
    _description = 'Stages'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')
    active = fields.Boolean(default=True)


class LocatieTag(models.Model):
    _name = 'locatie.tag'
    _description = 'Tags'

    name = fields.Char('Name')
    color = fields.Integer('Color')
    active = fields.Boolean(default=True)
