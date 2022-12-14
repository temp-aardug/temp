# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _

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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_aa_po_odoo_version = fields.Selection(
        version_list,
        string='Odoo Version',
        compute='_compute_odoo_version')
    x_aa_po_aardug_responsible = fields.Many2one(
        'hr.employee', string='Aardug Responsible',
        related='partner_id.x_aa_po_aardug_responsible')
    x_aa_po_aardug_project_leader = fields.Many2one(
        'hr.employee', string='Aardug Project Leader',
        related='partner_id.x_aa_po_aardug_project_leader')
    x_aa_po_hosting = fields.Selection(
        hosting_list, string='Hosting',
        compute='_compute_po_hosting')
    x_aa_po_project = fields.Many2one(
        'project.project', string='Customer Project',
        related='partner_id.project')
    x_aa_po_odoo_info = fields.Text(string='Odoo info')
    x_aa_po_expected_start_date = fields.Date(
        string='Expected Start Date')
    x_aa_po_expected_delivery_date = fields.Date(
        string='Expected Delivery Date')
    x_aa_po_real_start_date = fields.Date(
        string='Real Start Date')
    x_aa_po_real_delivery_date = fields.Date(
        string='Real Delivery Date')
    x_aa_po_project_leader_id = fields.Many2one(
        'res.partner', string='Project Leader Caret')
    x_aa_po_team_member_ids = fields.Many2many(
        'res.partner', string='Team Member Caret')
    x_aa_po_ticket = fields.Char(string='Ticket', )
    x_aa_po_ticket_nr = fields.Char(string='Ticket NR', )
    x_aa_po_status = fields.Char(string='Status', )
    x_aa_po_ticket_count = fields.Integer(
        string='Ticket Count', compute='_compute_ticket_count')
    x_aa_po_code = fields.Char(
        string='Task Numbers',
        required=True, default="/", readonly=True)
    xaa_aa_task_alias = fields.Many2one(
        'mail.alias', 'Alias', readonly=True)
    xaa_aa_attachment_ids = fields.One2many('ir.attachment',
                                            'x_aa_po_task_id',
                                            string='Attachments')
    x_aa_po_note = fields.Text(string='Note')
    x_aa_po_job_nr_caret = fields.Char(string='Job Nr Caret')
    x_aa_po_task_doc_ids = fields.One2many(
        'task.document', 'x_aa_task_id', string="Documents")

    @api.depends('partner_id')
    def _compute_odoo_version(self):
        """ Fetch odoo Version from partner and set that or set False"""
        for each in self:
            each.x_aa_po_odoo_version = \
                each.partner_id \
                and each.partner_id.x_aa_po_odoo_version or False

    @api.depends('partner_id')
    def _compute_po_hosting(self):
        """ Fetch PO Hosting from partner and set that or set False"""
        for each in self:
            each.x_aa_po_hosting = each.partner_id \
                                   and each.partner_id.x_aa_po_hosting \
                                   or False

    @api.onchange('partner_id')
    def onchange_partner(self):
        """ Fetch odoo from partner and set that or set False"""
        self.x_aa_po_odoo_info = self.partner_id.x_aa_po_odoo_info

    def _compute_ticket_count(self):
        """ Count number of tickets which are related to available task"""
        self.x_aa_po_ticket_count = self.env['helpdesk.ticket']. \
            search_count([('task_id', 'in', self.ids)])

    @api.model
    def default_get(self, fields):
        """ if Tickets are already there than set last
        ticket name,code and stage."""
        if self.x_aa_po_ticket_count >= 1:
            for ticket in self.project_id.ticket_ids:
                self.write({
                    'x_aa_po_ticket': ticket.name,
                    'x_aa_po_ticket_nr': ticket.x_aa_po_code,
                    'x_aa_po_status': ticket.stage_id.name, })
        return super(ProjectTask, self).default_get(fields)

    def action_ticket(self):
        """Open Task Related Tickets"""
        tickets = self.env['helpdesk.ticket'].search(
            [('task_id', '=', self.id)])
        return {
            'name': _('Tickets'),
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.ticket',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', tickets.ids)],
        }

    _sql_constraints = [
        ('project_task_unique_code', 'UNIQUE (x_aa_po_code)',
         _('The code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        """Create unique sequence number and mail alias"""
        if vals.get('x_aa_po_code', '/') == '/':
            vals['x_aa_po_code'] = self.env['ir.sequence']. \
                next_by_code('project.task')
        res = super(ProjectTask, self).create(vals)
        ir_model = self.env['ir.model'].search(
            [('model', '=', 'project.task')])
        user_id = res.user_ids and res.user_ids.ids[0] or False
        res.xaa_aa_task_alias = self.env['mail.alias'].sudo().create({
            'alias_name': res.x_aa_po_code,
            'alias_model_id': ir_model.id,
            'alias_defaults': {'x_aa_po_task_id': res.id},
            'alias_user_id': user_id
        }).id
        return res

    def copy(self, default=None):
        """Create unique sequence number on copy action"""
        if default is None:
            default = {}
        default['x_aa_po_code'] = self.env['ir.sequence']. \
            next_by_code('project.task')
        return super(ProjectTask, self).copy(default)

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Checked Documents are already there or
        not and added in message custom value"""
        if custom_values is None:
            custom_values = {}
        task = custom_values.get('x_aa_po_task_id', None)
        return task and self.browse(task) or super(
            ProjectTask, self).message_new(
            msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype_id=None, **kwargs):
        """ Checked if message type is email then set
        mt_comments and send that."""
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype_id = self.env.ref('mail.mt_comment').id
        return super(ProjectTask, self).message_post(
            subtype_id=subtype_id, **kwargs)

    def x_aa_po_email_sent_to_caret(self):
        """ Send  mail to caret with attachments of current record"""
        self.env['mail.mail'].sudo().create(
            {'subject': 'Mail From Aardug',
             'body_html': self.description,
             'email_to': 'configure.caret@gmail.com',
             'auto_delete': True,
             'email_from': (self.xaa_aa_task_alias.alias_name
                            + '@' + self.xaa_aa_task_alias.alias_domain
                            ),
             'attachment_ids': [
                 (4, att.id) for att in self.xaa_aa_attachment_ids],
             'reply_to': ''}
        ).sudo().send()
