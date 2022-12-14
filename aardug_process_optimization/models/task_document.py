# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class TaskDocument(models.Model):
    _name = 'task.document'
    _description = 'Documents'
    _rec_name = 'x_aa_po_task_doc_name'

    x_aa_po_task_doc_upload = fields.Binary(string='Upload Document')
    x_aa_po_task_doc_name = fields.Char(string='Doc Name', required=True)
    x_aa_task_id = fields.Many2one('project.task', string='Task')
