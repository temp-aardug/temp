# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _


class Locatie(models.Model):
    _name = 'locatie.locatie'
    _description = 'Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        '''To get default stage'''
        locatie_stages = self.env['locatie.stage'].search([])
        return locatie_stages[0] if locatie_stages else False

    @api.depends('stage_id')
    def _compute_kanban_state(self):
        '''Method to compute kanban state'''
        stage_new = self.env.ref('locaties.event_stage_new', raise_if_not_found=False)
        stage_inprogress = self.env.ref('locaties.event_stage_intreatment', raise_if_not_found=False)
        stage_done = self.env.ref('locaties.event_stage_ready', raise_if_not_found=False)
        stage_cancel = self.env.ref('locaties.event_stage_cancel', raise_if_not_found=False)
        for rec in self:
            rec.kanban_state = 'draft'
            if rec.stage_id.id == stage_new.id:
                rec.kanban_state = 'draft'
            elif rec.stage_id.id == stage_inprogress.id:
                rec.kanban_state = 'normal'
            elif rec.stage_id.id == stage_done.id:
                rec.kanban_state = 'done'
            elif rec.stage_id.id == stage_cancel.id:
                rec.kanban_state = 'blocked'

    @api.depends('partner_id')
    def _compute_helpdesk_ticket_count(self):
        ''' Method to compute kanban state'''

        helpdesk_ticket_obj = self.env["helpdesk.ticket"]
        for rec in self:
            rec.helpdesk_ticket_count = 0
            tickets_recs = helpdesk_ticket_obj.search_count([('locatie_id', '=', rec.id)])
            rec.helpdesk_ticket_count = tickets_recs

    @api.depends('partner_id')
    def _compute_maintenance_equipment_count(self):
        ''' Method to compute maintenance equipment count '''
        maintenance_equipment_obj = self.env["maintenance.equipment"]
        for rec in self:
            rec.maintenance_equipment_count = 0
            equipment_recs = maintenance_equipment_obj.search_count([('locatie_id', '=', rec.id)])
            rec.maintenance_equipment_count = equipment_recs

    @api.depends('partner_id')
    def _compute_maintenance_request_count(self):
        ''' Method o compute maintenance request count'''
        maintenance_request_obj = self.env["maintenance.request"]
        for rec in self:
            rec.maintenance_request_count = 0
            maintenance_request_recs = maintenance_request_obj.search_count([('locatie_id', '=', rec.id)])
            rec.maintenance_request_count = maintenance_request_recs

    name = fields.Char('Name')
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one(
        'res.partner',
        string="Contact",
        tracking=True
    )
    partner_phone = fields.Char('Telephone', tracking=True)
    partner_email = fields.Char('E-mail', tracking=True)
    user_id = fields.Many2one(
        'res.users',
        string='Responsible'
    )
    tag_ids = fields.Many2many(
        'locatie.tag',
        'locatie_tag_rel',
        'locatie_id', 'tag_id',
        string='Location Tags'
    )
    notes = fields.Html("Install information")
    maintenance_information = fields.Html("Maintenance information")
    priority = fields.Boolean("Priority")
    stage_id = fields.Many2one(
        'locatie.stage',
        ondelete='restrict',
        default=_get_default_stage_id,
        domain='[("active", "=", True)]',
        tracking=True,
        group_expand='_read_group_expand_full'
    )
    kanban_state = fields.Selection([
        ('draft', 'New'),
        ('normal', 'In Progress'),
        ('done', 'Done'),
        ('blocked', 'Blocked')],
        compute='_compute_kanban_state'
    )
    street = fields.Char("Street")
    postal_code = fields.Char("Postal Code")
    place = fields.Char("Place")
    photo = fields.Binary("Photo")
    desired_installation_date = fields.Date(
        "Desired installation date",
        default=lambda self: fields.Date.today()
    )
    longitude = fields.Float("Longitude")
    latitude = fields.Float("Latitude")
    product_ids = fields.Many2many(
        'product.product',
        'product_locatie_rel',
        'locatie_id', 'product_id',
        string="Products"
    )
    product_location_ids = fields.Many2many(
        'locatie.tag',
        'product_locatie_tag_rel',
        'locatie_id', 'pro_loc_id',
        string='Product Locations'
    )
    stock_lot_ids = fields.Many2many(
        'stock.lot',
        'stock_pro_locatie_rel',
        'locatie_id', 'stock_pro_id',
        string="Serial Number"
    )
    electricity_supply = fields.Char("Electricity supply")
    photo_1 = fields.Binary("Photo 1")
    photo_1_1 = fields.Binary("Photo 1")
    photo_2 = fields.Binary("Photo 2")
    photo_2_1 = fields.Binary("Photo 2")
    photo_3 = fields.Binary("Photo 3")
    photo_3_1 = fields.Binary("Photo 3")
    is_open_full_day = fields.Boolean("Open 24 hours a day")
    opening_hours = fields.Text("Opening hours during the week:")
    helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")
    maintenance_equipment_count = fields.Integer(compute="_compute_maintenance_equipment_count")
    maintenance_request_count = fields.Integer(compute="_compute_maintenance_request_count")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.write({
                'partner_phone': self.partner_id.phone,
                'partner_email': self.partner_id.email,
                'street': self.partner_id.street,
                'postal_code': self.partner_id.zip,
                'place': self.partner_id.city,
                'photo': self.partner_id.image_1920,
            })

    def action_open_helpdesk_ticket(self):
        '''this method is redirect the current records
        helpdesk ticket view from samrt button'''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "helpdesk.helpdesk_ticket_action_main_my")
        tickets = self.env['helpdesk.ticket'].search([
            ('locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', tickets.ids)]
        action['context'] = dict(
            self._context,
            default_locatie_id=self.id
        )
        return action

    def action_open_maintenance_equipment(self):
        '''this method is redirect the current records
        maintenance equipment view from amrt button'''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "maintenance.hr_equipment_action")
        equipments = self.env['maintenance.equipment'].search([
            ('locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', equipments.ids)]
        action['context'] = dict(
            self._context,
            default_locatie_id=self.id
        )
        return action

    def action_open_maintenance_request(self):
        '''this method is redirect the current records
        maintenance request view from amrt button'''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "maintenance.hr_equipment_request_action")
        maintenances = self.env['maintenance.equipment'].search([
            ('locatie_id', '=', self.id)])
        action['domain'] = [('id', 'in', maintenances.ids)]
        action['context'] = dict(
            self._context,
            default_locatie_id=self.id
        )
        return action
