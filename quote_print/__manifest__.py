# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Print Quotation',
    'category': 'Sale',
    'summary': 'Extend Functionality of Sale online quatation',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'version': '16.0.0',
    'description': ''' 
                1) This module main goal is build website quote report.
                2) Add report header/footer image and other configuration on
                   quotation template.
                3) web quote report have same content like website quote page.
                4) Sale order report use quotation template header/footer images
                   for report header/footer, and if there is no images then use
                   selected trademark configuration.
                5) Add digital signature field on user.
                6) Use custom object variable feature for get sale order any field
                   value on website quote (use code like $(custom:object.field_name)).
                7) Add new section(xaa_aa_website_desc_footer,
                   xaa_aa_website_desc_footer, xaa_aa_website_desc_footer_bellow)
                   in "sale_quotation_builder"
                8) customize on website quote page (pricing tab, first section 
                   on contact details, etc.)
                9) Add cover image and close image in report, this configure on
                   quotation template.
                10) Add mail template for quotation.
                11) Add remove footer checkbox on quotation template for hide
                    footer in web quote report.
                12) Hide pricing tab in report, if quotation template have
                    checkbox true for hide pricing tab, also hide it when
                    quotation total amount is 0,
                13) Remove the sale order line from the website quote, if that
                    line has optional products.
    ''',
    'depends': ['sale_management',
                'sale_quotation_builder',
                'custom_header_footer',
                'sale',
                'sale_margin',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/quote_custom_header.xml',
        'data/mail_template_data.xml',
        'data/partnership_contact_template.xml',
        'views/quote_print.xml',
        'views/res_users_view.xml',
        'views/quote_template.xml',
        'views/online_so_template.xml',
        'views/account_move.xml',
        'views/snippets.xml',
        'report/external_header_footer.xml',
        'report/quotation_report_first_page.xml',
        'report/quotation_report.xml',
        'report/sale_order_reports.xml',
        'report/cover_image_report.xml',
        'report/close_image_report.xml',
        'report/sale_report_template.xml',
        'report/invoice_report_template.xml',
    ],
    'demo': [
    ],
    'qweb': ['static/src/xml/hide_translation_msg.xml'],
    'installable': True,
    'license' : 'LGPL-3',

}
