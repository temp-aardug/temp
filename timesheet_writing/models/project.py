# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, models, fields


class Project(models.Model):
    _inherit = 'project.project'

    xaa_aa_total_project_cost = fields.Float(
        string='Cost', store=True,
        readonly=True, compute='_compute_total_project_cost')
    xaa_aa_project_work_type_ids = fields.One2many(comodel_name='project.work.type',
        inverse_name='xaa_aa_project_id', string='Work Type')
    xaa_aa_product_id = fields.Many2one('product.product', string='Travel Product')
    xaa_aa_sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    xaa_aa_task_id = fields.Many2one('project.task', string='Default Task Timesheet')

    @api.depends('task_ids.xaa_aa_total_task_cost')
    def _compute_total_project_cost(self):
        for rec in self:
            rec.xaa_aa_total_project_cost = sum(
                [line.xaa_aa_total_task_cost for line in rec.task_ids])


class ProjectWorkType(models.Model):
	_name = 'project.work.type'
	_description = 'Project Work Type'
	_rec_name = 'xaa_aa_work_type_id'

	xaa_aa_work_type_id = fields.Many2one('timesheet.work.type', string='Work Type')
	xaa_aa_cost = fields.Float('Cost')
	xaa_aa_project_id = fields.Many2one('project.project', string='Project')
