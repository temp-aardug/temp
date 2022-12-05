# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
import logging
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
_MAP_COLORS = {
  'oranje': 8,
  'red': 9,
  'green': 7,
  'purple': 6,
}


class CrmLead(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    xaa_aa_remainder_mail = fields.Boolean(string='FollowUp Mail')
    xaa_aa_warning_mail = fields.Boolean(string='Reminder Mail')
    xaa_aa_custom_ids = fields.Many2many('crm.stage.custom', string='Performed Actions')

    @api.model
    def create(self, vals):
        """ Creates Crm Lead"""
        res = super(CrmLead, self).create(vals)
        if vals.get('partner_id') and vals.get('partner_id') not in [
            x.partner_id.id for x in self.message_follower_ids]:
            res.message_subscribe([vals.get('partner_id')])
        return res

    def write(self, vals):
        """ It updates FollowUp Mail, Reminder Mail, Performed Actions and message_partner_ids"""
        if vals.get('partner_id') and vals.get('partner_id') not in [
            x.partner_id.id for x in self.message_follower_ids]:
            self.message_subscribe([vals.get('partner_id')])
        if 'stage_id' in vals:
            vals.update(xaa_aa_remainder_mail=False,
                        xaa_aa_warning_mail=False,
                        message_partner_ids=[(4, self.partner_id.id)],
                        xaa_aa_custom_ids=[(5, 0, 0)])
        return super(CrmLead,self).write(vals)

    @api.model
    def send_mail(self, custom):
        ''' send mail to opportunity customer based on crm stage configuration'''
        Mail = self.env['mail.mail']
        MailCompose = self.env['mail.compose.message']
        IrModel = self.env['ir.model.data']
        Fields = ['subject', 'body_html', 'email_from', 'email_to', 'partner_to',
        'email_cc',  'reply_to', 'attachment_ids', 'mail_server_id']
        for rec in self:
            template = MailCompose.generate_email_for_composer(
                custom.xaa_aa_template_id.id, rec.id, Fields)
            mail_id = Mail.create({
                'auto_delete': False,
                'email_to': rec.email_from,
                'subject': template.get('subject'),
                'body_html': template.get('body'),
                'author_id': 3,
            })
            if not rec.partner_id:
                mail_id.mail_message_id.write({
                    'model':'crm.lead',
                    'body': mail_id.body_html,
                    'res_id' : rec.id,
                    'message_type' : 'comment',
                    'subtype_id': IrModel._xmlid_to_res_id('mail.mt_comment'),
                    'record_name': rec.name,
                  })
            mail_id.send()
            rec.message_post(
                body=mail_id.body_html,
                subject=mail_id.subject,
                message_type='comment',
                subtype_id=IrModel._xmlid_to_res_id('mail.mt_comment'),
            )
            mail_id.unlink()
        return True

    def compare_date(self, date, after_before, real_date):
        """ This compares date"""
        duration, unit = date.split('_')
        if(unit == "m"):
            return real_date + datetime.timedelta(minutes=int(duration))
        hours = int(duration) if unit == "h" else int(duration) * 24
        return real_date + datetime.timedelta(
            hours=hours * -1 if after_before == 'before' else hours * 1)

    def _create_meeting(self, custAct, rec, dateDeadline):
        ''' create meeting based on configuration on crm stage'''
        user = rec.user_id if rec.user_id else custAct.xaa_aa_user_id
        self.env['calendar.event'].create({
            'name': custAct.xaa_aa_name +' - '+ rec.name,
            'opportunity_id': rec.id,
            'partner_ids': [[6, False, [user.partner_id.id]]],
            'user_id': user.id,
            'start': dateDeadline,
            'stop': dateDeadline + relativedelta(minutes=30),
            'description': custAct.xaa_aa_note,
        })

    def _do_custom_action(self, rec, stage, current_date):
        ''' create activity based on configuration in crm stage'''
        custAct = stage.xaa_aa_custom_action_id
        custTime = int(custAct.xaa_aa_time)
        userId = rec.user_id if rec.user_id else custAct.xaa_aa_user_id
        if userId:
            crmModel = self.env['ir.model'].search(
                [('model', '=', 'crm.lead')], limit=1)
            if custAct.xaa_aa_period == 'day':
                dateDeadline = current_date + relativedelta(days=custTime)
            if custAct.xaa_aa_period == 'month':
                dateDeadline = current_date + relativedelta(months=custTime)
            if custAct.xaa_aa_period == 'year':
                dateDeadline = current_date + relativedelta(years=custTime)

            self.env['mail.activity'].create({
                'res_id': rec.id,
                'res_model_id': crmModel.id,
                'activity_type_id': custAct.xaa_aa_next_activity_id.id,
                'note': custAct.xaa_aa_note,
                'date_deadline': dateDeadline,
                'user_id': userId.id,
            })
            if custAct.xaa_aa_next_activity_id.category == 'meeting':
                self._create_meeting(custAct, rec, dateDeadline)
            rec.xaa_aa_custom_ids = [(4, stage.id)]

    @api.model
    def email_send_stages(self):
        """ This cron job send mail to customer according configuration on crm stage"""
        stage_custom_ids = self.env['crm.stage.custom'].search(
            [('xaa_aa_send_mail', '=', True), ('xaa_aa_crm_stage_id', '!=', False)])
        for stage in stage_custom_ids:
            if stage.xaa_aa_mail_action == 'remainder':
                rec_ids = self.search(
                    [('type', '=', 'opportunity'),
                    ('stage_id', '=', stage.xaa_aa_crm_stage_id.id),
                    ('xaa_aa_remainder_mail', '=', False)])
            else:
                rec_ids = self.search(
                    [('type', '=', 'opportunity'),
                    ('stage_id', '=', stage.xaa_aa_crm_stage_id.id),
                    ('xaa_aa_warning_mail', '=', False)])
            when = stage.xaa_aa_action_when
            field = stage.xaa_aa_action_perform
            _logger.info('crm kanban records......%s',rec_ids)
            for rec in rec_ids:
                try:
                    value = getattr(rec, field.xaa_aa_key) if hasattr(rec, field.xaa_aa_key) else False
                    if value:
                        if field.xaa_aa_field_id.ttype == 'datetime':
                            date = value
                            date_to_compare = self.compare_date(stage.xaa_aa_action_time, when, date)
                            current_date = datetime.datetime.now()
                        else:
                            date = value
                            date_to_compare = self.compare_date(stage.xaa_aa_action_time, when, date)
                            current_date = datetime.date.today()
                        if ((date >= current_date >= date_to_compare and when == "before") or (
                            when == "after" and current_date >= date_to_compare)):
                            if stage.xaa_aa_mail_action == 'remainder':
                                rec.send_mail(stage)
                                rec.xaa_aa_remainder_mail = True
                            if stage.xaa_aa_mail_action == 'warning':
                                rec.send_mail(stage)
                                rec.xaa_aa_warning_mail = True
                            if stage.xaa_aa_custom_action_id and not stage in rec.xaa_aa_custom_ids:
                                self._do_custom_action(rec, stage, current_date)
                except Exception as e:
                    _logger.error("Error in record <%s>, so skipped this record to fix mail issue ", rec.id)
                    continue

    def read(self, fields=None, load='_classic_read'):
        ''' Add color in crm kanban records based on crm stage configuration'''
        records = super(CrmLead, self).read(fields=fields, load=load)
        crm_stage = self.env['crm.stage']
        def compare_date(date, after_before, real_date):
            duration, unit = date.split('_')
            if(unit == "m"):
                return real_date + datetime.timedelta(minutes=int(duration))
            hours = int(duration) if unit == "h" else int(duration) * 24
            return real_date + datetime.timedelta(
                hours=hours * -1 if after_before == 'before' else hours * 1)
        for rec in records:
            stage_id =  rec.get('stage_id')[0] if isinstance(rec.get('stage_id'), tuple) else rec.get('stage_id')
            crm_browse = crm_stage.browse(stage_id)
            if rec.get('color') in [6,7,8,9]:rec['color'] = 0
            for custom in crm_browse.xaa_aa_custom_ids:
                when, field = custom.xaa_aa_action_when, custom.xaa_aa_action_perform
                value = rec.get(field.xaa_aa_key)
                if value:
                    if field.xaa_aa_field_id.ttype == 'datetime':
                        date = value
                        date_to_compare = compare_date(custom.xaa_aa_action_time, when, date)
                        current_date = datetime.datetime.now()
                    else:
                        date = value
                        date_to_compare = compare_date(custom.xaa_aa_action_time, when, date)
                        current_date = datetime.date.today()
                    if (date >= current_date >= date_to_compare and when == "before") or (
                        when == "after" and current_date >= date_to_compare):
                        rec['color'] = _MAP_COLORS[custom.xaa_aa_action_color]
        return records


class CrmStage(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.stage"

    xaa_aa_custom_ids = fields.One2many('crm.stage.custom', 'xaa_aa_crm_stage_id',
        string='Kanban Custom')


class OpportunityActionConfig(models.Model):
    _name = 'opportunity.action.config'
    _description = "opportunity config action"
    _rec_name = 'xaa_aa_name'

    xaa_aa_name = fields.Char(string='Name')
    xaa_aa_next_activity_id = fields.Many2one('mail.activity.type', string='Next Activity')
    xaa_aa_time = fields.Char(string='Time')
    xaa_aa_period = fields.Selection([('day', 'Day'), ('month', 'Month'), ('year', 'Year')],
        string='Period')
    xaa_aa_note = fields.Text(string='Note')
    xaa_aa_user_id = fields.Many2one('res.users', string='User')


class CrmFieldConfiguration(models.Model):
    _name = 'crm.field.config'
    _description = "CRM Field Configuration"
    _rec_name = 'xaa_aa_name'

    xaa_aa_name = fields.Char(string='Field Label')
    xaa_aa_key = fields.Char(string='Key')
    xaa_aa_field_id = fields.Many2one('ir.model.fields', string='Field',
        domain=[('model', '=', 'crm.lead'), ('ttype', 'in', ['date', 'datetime'])])

    @api.onchange('xaa_aa_field_id')
    def onchange_field(self):
        self.write({
            'xaa_aa_name': self.xaa_aa_field_id.field_description,
            'xaa_aa_key': self.xaa_aa_field_id.name
        })


class CrmStageCustom(models.Model):
    _name = "crm.stage.custom"
    _order = 'xaa_aa_priority desc'
    _rec_name = 'xaa_aa_custom_action_id'
    _description = "CRM Stage Line"

    xaa_aa_priority = fields.Integer(string='Priority', default=1, required=True)
    xaa_aa_send_mail = fields.Boolean('Send mail')
    xaa_aa_template_id = fields.Many2one('mail.template', string='Template')
    xaa_aa_crm_stage_id = fields.Many2one('crm.stage', string='Stage')
    xaa_aa_action_when = fields.Selection(
    [('before', 'Before'), ('after', 'After')], string='Before/After', required=True)
    xaa_aa_custom_action_id = fields.Many2one('opportunity.action.config',
        string='Custom Action')
    xaa_aa_mail_action = fields.Selection(
        [('remainder', 'FollowUp Mail'), ('warning', 'Reminder Mail')], string='Mail Action')
    xaa_aa_action_time = fields.Selection(
        [('5_m', '5 Minutes'), ('15_m', '15 Minutes'), ('30_m', '30 Minutes'), 
        ('1_h', '1 Hour'), ('2_h', '2 Hours'), ('4_h', '4 Hours'), ('8_h', '8 Hours'),
        ('1_d', '1 Day'), ('2_d', '2 Days'), ('3_d', '3 Days'), ('4_d', '4 Days'),
        ('5_d', '5 Days'), ('7_d', '7 Days'), ('10_d', '10 Days'), ('20_d', '20 Days'),
        ('30_d', '30 Days'), ('180_d', '180 Days'), ('365_d', '365 Days')],
        string='Time', required=True)
    xaa_aa_action_color = fields.Selection(
        [('oranje', 'Orange'), ('red', 'Red'), ('green', 'Green'), ('purple', 'Purple')],
        string='Colors', required=True)
    xaa_aa_action_perform = fields.Many2one('crm.field.config', required=True, string='Action perform')

    @api.constrains('xaa_aa_action_time', 'xaa_aa_saction_perform')
    def _check_action_time(self):
        """ Check actions """
        for rec in self:
            if (rec.xaa_aa_action_perform.xaa_aa_field_id.ttype == 'date' and
                rec.xaa_aa_action_time in ['1_m','5_m','15_m','30_m','1_h','2_h','4_h','8_h']):
                raise ValidationError(_('Misconfiguration, check Field and Time.'))
