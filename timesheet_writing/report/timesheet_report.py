# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, models


class ReportTimesheetWriting(models.AbstractModel):
    _name = 'report.hr_timesheet.report_timesheet'
    _description = 'Hr Timesheet Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.analytic.line'].browse(docids)
        date_lst = [x.date for x in docs]
        emp_dict = {}
        for emp in docs.mapped('employee_id'):
            analytic_ids = docs.filtered(lambda rec: rec.employee_id == emp)
            emp_dict[emp.name] = sum(analytic_ids.mapped('unit_amount'))
        return {
            'doc_ids': docids,
            'doc_model': 'account.analytic.line',
            'data': data,
            'docs': docs,
            'min_date': min(date_lst),
            'max_date': max(date_lst),
            'project_ids': docs.mapped('project_id'),
            'emp_dict': emp_dict,
        }
