# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _compute_user_lang(self):
        for rec in self:
            rec.user_lang = self.env['res.lang']._lang_get(self.env.user.lang).name

    locaties_ids = fields.Many2many(
        'locatie.locatie',
        'locatie_partner_rel',
        'partner_id', 'locatie_id',
        string="Locaties"
    )
    user_lang = fields.Char(compute="_compute_user_lang")


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    locatie_id = fields.Many2one(
        'locatie.locatie',
        string='Location'
    )
