# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    xaa_aa_product_cost = fields.Float('Cost')
    xaa_aa_account_move_id = fields.Many2one('account.move', string='Journal Entries')
    xaa_aa_make_accounting_entry = fields.Boolean(default=True, string='Make Accounting Entry')
    xaa_aa_long_description = fields.Text(string='Long Description')
    xaa_aa_image_up = fields.Binary('Image', attachment=True)

    def get_default_task(self, project):
        '''Method called from js-rpc to fill project default task automatically to portal'''
        project_default_task = self.env['project.project'].browse(
            int(project)).xaa_aa_task_id.id
        return project_default_task

    def action_view_analytic_line_long_desc(self):
        '''render long description form view on icon click'''
        return {
            'name': _('Long Description'),
            'view_mode': 'form',
            'res_model': 'account.analytic.line',
            'view_id': self.env.ref(
                'timesheet_writing.view_account_analytic_line_form_desc').id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
        }

    def action_view_analytic_line_img(self):
        '''render imange upload form view on icon click'''
        return {
            'name': _('Image'),
            'view_mode': 'form',
            'res_model': 'account.analytic.line',
            'view_id': self.env.ref(
                'timesheet_writing.view_account_analytic_line_form_img').id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
        }

    def _timesheet_postprocess_values(self, values):
        ''' Get the addionnal values to write on record
            :param dict values: values for the model's fields, as a dictionary::
                {'field_name': field_value, ...}
            :return: a dictionary mapping each record id to its corresponding
                dictionnary values to write (may be empty).
        '''
        result = {id_: {} for id_ in self.ids}
        sudo_self = self.sudo()  # this creates only one env for all operation that required sudo()
        # (re)compute the amount (depending on unit_amount, employee_id for the cost, and account_id for currency)
        if any([field_name in values for field_name in [
            'work_type_id', 'unit_amount', 'employee_id', 'account_id']]):
            for timesheet in sudo_self:
                if timesheet.work_type_id and timesheet.work_type_id.xaa_aa_product_id:
                    prod_accounts = timesheet.work_type_id.xaa_aa_product_id.product_tmpl_id._get_product_accounts()
                    unit = timesheet.work_type_id.xaa_aa_product_id.uom_id
                    account = prod_accounts['expense']
                    cost = timesheet.work_type_id.xaa_aa_product_id.price_compute(
                        'standard_price', uom=unit)[timesheet.work_type_id.xaa_aa_product_id.id]
                    for project in timesheet.task_id.project_id.xaa_aa_project_work_type_ids:
                        if project.xaa_aa_work_type_id == timesheet.work_type_id:
                            if project.xaa_aa_cost < 1:
                                project.xaa_aa_cost = cost
                            cost = project.xaa_aa_cost
                        else:
                            project.create({
                                'xaa_aa_work_type_id': timesheet.work_type_id.id,
                                'xaa_aa_cost': cost,
                                'xaa_aa_project_id': timesheet.task_id.project_id.id
                            })
                    if not timesheet.task_id.project_id.xaa_aa_project_work_type_ids:
                        timesheet.task_id.project_id.xaa_aa_project_work_type_ids.create({
                            'xaa_aa_work_type_id': timesheet.work_type_id.id,
                            'xaa_aa_cost': cost,
                            'xaa_aa_project_id': timesheet.task_id.project_id.id
                        })
                else:
                    cost = timesheet._hourly_cost()
                amount = -timesheet.unit_amount * cost
                amount_converted = timesheet.employee_id.currency_id._convert(
                    amount, timesheet.account_id.currency_id, self.env.company, timesheet.date)
                result[timesheet.id].update({
                    'amount': amount_converted,
                    'xaa_aa_product_cost': amount_converted * (-1),
                    'product_id': timesheet.work_type_id.xaa_aa_product_id.id
                })
        return result
