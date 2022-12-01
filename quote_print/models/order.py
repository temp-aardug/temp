# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import base64
from odoo import api, fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    xaa_aa_website_desc_footer = fields.Html('Template Footer', translate=True)
    xaa_aa_website_desc_footer_bellow = fields.Html('Template Footer Below',
        translate=True)
    xaa_aa_show_only_total = fields.Boolean('Show Only Total', default=True)
    xaa_aa_cover_image = fields.Binary("Cover Image", store=True)
    xaa_aa_close_image = fields.Binary('Closing Image')

    def action_quotation_send(self):
        ''' this method use to set email template which is set in Quotation Template  '''
        res = super(SaleOrderInherit, self).action_quotation_send()
        if self.state == 'sale':
            confirmed_mail = self.env.ref('sale.mail_template_sale_confirmation', False)
            res['context']['default_template_id'] = confirmed_mail and confirmed_mail.id
        return res

    # def check_line_description(self):
    #     ''' this method will check sale order has multiple same product
    #         then it will return only single order line for print it's description
    #         on report.
    #     '''
    #     order_product = []
    #     order_line = []
    #     for line in self.order_line:
    #         if line.product_id not in order_product:
    #             order_product.append(line.product_id)
    #             order_line.append(line.id)
    #     sale_order_line = self.env['sale.order.line'].browse(order_line)
    #     return sale_order_line


    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        '''This method is remove from base so just custom functinality add in this method'''
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
        self.write({
            'website_description' : template.website_description,
            'xaa_aa_website_desc_footer' : template.xaa_aa_website_desc_footer,
            'xaa_aa_website_desc_footer_bellow' : template.xaa_aa_website_desc_footer_bellow,
            'xaa_aa_cover_image' : template.xaa_aa_cover_image,
            'xaa_aa_close_image' : template.xaa_aa_close_image
        })

    def get_quote_print_pdf(self):
        return self.env.ref('quote_print.report_web_quotation_custom').report_action(
            self, config=False)


class SaleQuoteTemplateInh(models.Model):
    _inherit = 'sale.order.template'

    xaa_aa_website_desc_footer = fields.Html('Template Footer', translate=True)
    xaa_aa_website_desc_footer_bellow = fields.Html('Template Footer Below',
        translate=True)
    xaa_aa_cover_image = fields.Binary("Cover Image", attachment=True)
    xaa_aa_file_name_cover = fields.Char('File Name')
    xaa_aa_cover_image_pdf = fields.Binary("Cover Image Pdf", attachment=True)
    xaa_aa_report_layout = fields.Selection([
         ('address_only', 'First Page Address Only'),
         ('no_extra_space', 'Start Content From First Page')],
         string='Report Layout')
    xaa_aa_file_name_cover_pdf = fields.Char('Pdf File Name')
    xaa_aa_cover_height = fields.Integer(string="Cover Image Height",
        default=1031)
    xaa_aa_isfooteradrsimg_first_page = fields.Boolean(
        string="Remove Footer",
        help="Show footer address image on first\
        page when rest pages don't have footer")
    xaa_aa_close_image = fields.Binary('Closing Image', attachment=True)
    xaa_aa_close_height = fields.Integer(string="Closing Image Height",
        default=1031)
    xaa_aa_file_name_close = fields.Char('Close File Name')
    xaa_aa_close_image_pdf = fields.Binary("Close Image Pdf", attachment=True)
    xaa_aa_file_name_close_pdf = fields.Char('Pdf File name')
    xaa_aa_header_image = fields.Binary("Header Image")
    xaa_aa_file_name_header = fields.Char('Header File name')
    xaa_aa_footer_image = fields.Binary("Footer Image")
    xaa_aa_file_name_footer = fields.Char('Footer File Name')
    xaa_aa_file_name_pdf = fields.Char('PDF File Name')
    xaa_aa_hide_pricing_tab = fields.Boolean(string='Hide Pricing Tab')

    @api.model
    def create(self, values):
        result = super(SaleQuoteTemplateInh, self).create(values)
        if result.xaa_aa_cover_image:
            result.generate_pdf()
        if result.xaa_aa_close_image:
            result.generate_pdf()
        return result

    def write(self, values):
        result = super(SaleQuoteTemplateInh, self).write(values)
        if (self.xaa_aa_cover_image and values.get('xaa_aa_cover_height')) or \
            (self.xaa_aa_close_image and values.get('xaa_aa_close_height')):
            self.generate_pdf()
        return result

    def generate_pdf(self):
        if not self.xaa_aa_cover_image:
            self.write({
                'xaa_aa_cover_image_pdf': None,
                'self.xaa_aa_file_name_cover_pdf':None
            })
        else:
            reportAct = self.env.ref('quote_print.report_web_quote_cover')
            if reportAct:
                pdf_bin, _ = reportAct._render_qweb_pdf(reportAct.report_name,
                    res_ids=reportAct.id)
                self.xaa_aa_cover_image_pdf = base64.b64encode(pdf_bin)
                self.xaa_aa_file_name_cover_pdf = (self.xaa_aa_file_name_cover.split('.')[0] or 'cover') + '.pdf'
        if not self.xaa_aa_close_image:
            self.write({
                'xaa_aa_close_image_pdf': None,
                'self.xaa_aa_file_name_close_pdf':None
            })
        else:
            if self:
                reportCloseAct = self.env.ref('quote_print.report_web_quote_close')
                if reportCloseAct:
                    closepdf_bin, _ = reportCloseAct._render_qweb_pdf(
                        reportCloseAct.report_name,res_ids=reportCloseAct.id)
                    self.write({
                        'xaa_aa_close_image_pdf' : base64.b64encode(closepdf_bin),
                        'xaa_aa_file_name_close_pdf' : (
                            self.xaa_aa_file_name_close.split('.')[0] or 'close') + '.pdf'
                    })
