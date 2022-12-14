# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models

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


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    x_aa_po_customer_company_id = fields.Many2one(
        'res.partner',
        string="Customer Company")
    x_aa_po_odoo_version = fields.Selection(
        version_list,
        string='Odoo Version',
        compute='_compute_odoo_version')
    x_aa_po_aardug_responsible = fields.Many2one(
        'hr.employee',
        string='Aardug Responsible',
        related='x_aa_po_customer_company_id.x_aa_po_aardug_responsible')
    x_aa_po_aardug_project_leader = fields.Many2one(
        'hr.employee',
        string='Aardug Project Leader',
        related='x_aa_po_customer_company_id.x_aa_po_aardug_project_leader')
    x_aa_po_hosting = fields.Selection(
        hosting_list,
        string='Hosting',
        compute='_compute_po_hosting')
    x_aa_po_project = fields.Many2one(
        'project.project',
        string='Customer Project',
        related='x_aa_po_customer_company_id.project')
    x_aa_po_odoo_info = fields.Text(string='Odoo info', )
    x_aa_po_code = fields.Char(
        string='Ticket Number',
        default="#", required=True, readonly=True)
    x_aa_po_ticket_alias = fields.Many2one('mail.alias',
                                           'Alias',
                                           readonly=True)
    x_aa_po_attachment_ids = fields.One2many('ir.attachment',
                                             'x_aa_po_ticket_id',
                                             string='Attachments')
    task_id = fields.Many2one(
        "project.task", string="Task",
        compute='_compute_task_id',
        store=True, readonly=False,
        domain="[('id', 'in', _related_task_ids)]",
        tracking=True,
        help="The task must have the same customer as this ticket.")

    _related_task_ids = fields.Many2many(
        'project.task',
        compute='_compute_related_task_ids')

    @api.depends('project_id')
    def _compute_task_id(self):
        """ Checked Task is related with different
        project than set task value is False."""
        self.filtered(
            lambda t: t.project_id != t.task_id.project_id).update(
            {'task_id': False})

    @api.depends('project_id', 'company_id')
    def _compute_related_task_ids(self):
        """ Set Related task which are related to
         same company and Project with timesheet boolean."""
        for ticket in self:
            ticket._related_task_ids = self.env['project.task']. \
                search(ticket.project_id and [
                ('project_id', '=', ticket.project_id.id)] or [
                           ('project_id.allow_timesheets', '=', True),
                           ('company_id', '=', ticket.company_id.id)])._origin

    @api.depends('x_aa_po_customer_company_id')
    def _compute_odoo_version(self):
        """ Fetch odoo Version from customer company and
        set that or set False"""
        for each in self:
            each.x_aa_po_odoo_version = \
                each.x_aa_po_customer_company_id \
                and each.x_aa_po_customer_company_id.x_aa_po_odoo_version \
                or False

    @api.depends('x_aa_po_customer_company_id')
    def _compute_po_hosting(self):
        """ Fetch PO Hosting from customer company and set that or set
        False"""
        for each in self:
            each.x_aa_po_hosting = \
                each.x_aa_po_customer_company_id \
                and each.x_aa_po_customer_company_id.x_aa_po_hosting or False

    @api.onchange('partner_id')
    def onchange_partner(self):
        """ Fetch project and customer company from partner
        parent and set that ,also fetch odoo info from partner"""
        self.write(
            {
                'project_id': self.partner_id.parent_id.project,
                'x_aa_po_odoo_info': self.partner_id.x_aa_po_odoo_info,
                'x_aa_po_customer_company_id': self.partner_id.parent_id,
            }
        )

    @api.model
    def create(self, vals):
        """ Create Ticket Alias ,Fetch project and
        customer company from partner parent"""
        res = super(HelpdeskTicket, self).create(vals)
        if res.display_name:
            res.x_aa_po_code = 'H' + str(res.id)
        ir_model = self.env['ir.model'].search(
            [('model', '=', 'helpdesk.ticket')])
        res.x_aa_po_ticket_alias = self.env['mail.alias'].sudo().create({
            'alias_name': res.x_aa_po_code,
            'alias_model_id': ir_model.id,
            'alias_defaults': {'x_aa_po_ticket_id': res.id},
            'alias_user_id': res.user_id.id
        }).id
        if not res.x_aa_po_customer_company_id and res.partner_id:
            res.x_aa_po_customer_company_id = res.partner_id.parent_id \
                                              and res.partner_id.parent_id.id \
                                              or False
        if res.partner_id and res.partner_id.parent_id \
                and res.partner_id.parent_id.project:
            res.project_id = res.partner_id.parent_id.project.id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Checked Documents are already there or
        not and added in message custom value"""
        if custom_values is None:
            custom_values = {}
        task = custom_values.get('x_aa_po_ticket_id', None)
        return task and self.browse(task) or super(
            HelpdeskTicket, self).message_new(
            msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype_id=None, **kwargs):
        """ Checked if message type is email then set
        mt_comments and send that."""
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype_id = self.env.ref('mail.mt_comment').id
        return super(HelpdeskTicket, self).message_post(
            subtype_id=subtype_id, **kwargs)

    def copy(self, default=None):
        """ Create Sequence while Helpdesk duplicate"""
        if default is None:
            default = {}
        default['x_aa_po_code'] = self.env['ir.sequence']. \
            next_by_code('helpdesk.ticket')
        return super(HelpdeskTicket, self).copy(default)

    def create_task(self):
        """ Create Task if project is there and set that in task field."""
        if self.project_id:
            task_id = self.env['project.task'].create(
                {'name': self.display_name,
                 'project_id': self.project_id.id,
                 'partner_id': self.partner_id and self.partner_id, })
            self.task_id = task_id
