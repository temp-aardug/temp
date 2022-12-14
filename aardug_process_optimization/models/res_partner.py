# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models

version_list = [
    ('odoo_8', 'Odoo 8'),
    ('odoo_9', 'Odoo 9'),
    ('odoo_10', 'Odoo 10'),
    ('odoo_11', 'Odoo 11'),
    ('odoo_12', 'Odoo 12'),
    ('odoo_13', 'Odoo 13'),
    ('odoo_14', 'Odoo 14'),
    ('odoo_15', 'Odoo 15'),
    ('odoo_16', 'Odoo 16'),
]
hosting_list = [
    ('odoo_saas', 'Odoo SaaS'),
    ('odoo_sh', 'Odoo.sh'),
    ('aws', 'AWS'),
    ('eigen', 'EIGEN'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_aa_po_odoo_version = fields.Selection(
        version_list, string='Odoo Version')
    x_aa_po_aardug_responsible = fields.Many2one(
        'hr.employee', string='Aardug Responsible')
    x_aa_po_aardug_project_leader = fields.Many2one(
        'hr.employee', string='Aardug Project Leader')
    x_aa_po_hosting = fields.Selection(hosting_list, string='Hosting')
    project = fields.Many2one('project.project', string='Project')
    x_aa_po_odoo_info = fields.Text(string='Odoo info')
