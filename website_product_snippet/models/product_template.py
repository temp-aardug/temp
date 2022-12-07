# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api
from bs4 import BeautifulSoup
from markupsafe import Markup


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #Solar Panel Snippet
    xaa_ec_logo = fields.Binary('Logo ')
    xaa_ec_product_image = fields.Binary('Item Picture')
    xaa_ec_product_image_opt = fields.Binary('Item Picture 2')
    xaa_ec_point1_icon = fields.Binary('Point 1 Icon')
    xaa_ec_point1_title = fields.Char('Point 1 Title')
    xaa_ec_point1_desc = fields.Text('Point 1 Description')
    xaa_ec_point2_icon = fields.Binary('Point 2 Icon')
    xaa_ec_point2_title = fields.Char('Point 2 Title')
    xaa_ec_point2_desc = fields.Text('Point 2 Description')
    xaa_ec_point3_icon = fields.Binary('Point 3 Icon')
    xaa_ec_point3_title = fields.Char('Point 3 Title')
    xaa_ec_point3_desc = fields.Text('Point 3 Description')
    xaa_ec_point4_icon = fields.Binary('Point 4 Icon')
    xaa_ec_point4_title = fields.Char('Point 4 Title')
    xaa_ec_point4_desc = fields.Text('Point 4 Description')
    xaa_ec_point5_icon = fields.Binary('Point 5 Icon')
    xaa_ec_point5_title = fields.Char('Point 5 Title')
    xaa_ec_point5_desc = fields.Text('Point 5 Description')
    xaa_ec_desciption = fields.Selection(
                            [('automatic','Automatic'),
                            ('manually','Manual')
                            ],
                            string='Description Visiblity', default='manually')


    def _set_website_snippet_description(self):
        desc_text = """
            <section class="s_text_image pt32 pb32 o_colored_level" 
            data-snippet="solar_panel_product_snippet" 
            data-name="Logo - Text - Icon" 
            style="background-image: none;">
                <div class="container">
                    <div class="row align-items-center">
                        <div class="pt16 pb16 col-lg-5 o_colored_level">
                            <div>
                                <img id="xaa_ec_logo" 
                                class="img img-fluid mx-auto padding-xl" 
                                src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_logo" 
                                loading="lazy">
                            </div>
                            <p style="font-size: 20px;">
                            <b>"""+str(self.name if self.name else 'A Section Title')+"""</b></p>
                            <div class="col-lg-12">
                                <div class="row">
                                    <div style="width:10%;" class="o_colored_level">
                                        <img id="xaa_ec_point1_icon" 
                                        class="img img-fluid mx-auto" 
                                        src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_point1_icon" 
                                        loading="lazy">
                                    </div>
                                    <div style="width:80%;margin:6px;" class="o_colored_level">
                                        <p style="margin: auto; font-size: 16px;">
                                        <b>"""+str(self.xaa_ec_point1_title if self.xaa_ec_point1_title else "A Point 1 Title")+"""</b></p>
                                        <p style="font-size: 14px;">
                                        """+str(self.xaa_ec_point1_desc if self.xaa_ec_point1_desc else "Write one or two paragraphs describing your point 1.")+"""</p>
                                    </div>
                                </div>
                                <div class="row">
                                    <div style="width:10%;" class="o_colored_level">
                                        <img id="xaa_ec_point2_icon" 
                                        class="img img-fluid mx-auto" 
                                        src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_point2_icon" 
                                        loading="lazy">
                                    </div>
                                    <div style="width:80%;margin:6px;" class="o_colored_level">
                                        <p style="margin: auto; font-size: 16px;"><b>
                                        """+str(self.xaa_ec_point2_title if self.xaa_ec_point2_title else "A Point 2 Title")+"""</b></p>
                                        <p style="font-size: 14px;">
                                        """+str(self.xaa_ec_point2_desc if self.xaa_ec_point2_desc else "Write one or two paragraphs describing your point 2.")+"""</p>
                                    </div>
                                </div>
                                <div class="row">
                                    <div style="width:10%;" class="o_colored_level">
                                        <img id="xaa_ec_point3_icon" 
                                        class="img img-fluid mx-auto" 
                                        src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_point3_icon" 
                                        loading="lazy">
                                    </div>
                                    <div style="width:80%;margin:6px;" class="o_colored_level">
                                        <p style="margin: auto; font-size: 16px;"><b>
                                        """+str(self.xaa_ec_point3_title if self.xaa_ec_point3_title else "A Point 3 Title")+"""</b></p>
                                        <p style="font-size: 14px;">
                                        """+str(self.xaa_ec_point3_desc if self.xaa_ec_point3_desc else "Write one or two paragraphs describing your point 3.")+"""</p>
                                    </div>
                                </div>
                    """
        if self.xaa_ec_point4_icon and self.xaa_ec_point4_title and self.xaa_ec_point4_desc:
            desc_text += """
                        <div class="row">
                            <div style="width:10%;" class="o_colored_level">
                                <img id="xaa_ec_point4_icon" 
                                class="img img-fluid mx-auto" 
                                src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_point4_icon" 
                                loading="lazy">
                            </div>
                            <div style="width:80%;margin:6px;" class="o_colored_level">
                                <p style="margin: auto; font-size: 16px;"><b>
                                """+str(self.xaa_ec_point4_title if self.xaa_ec_point4_title else "A Point 4 Title")+"""</b></p>
                                <p style="font-size: 14px;">
                                """+str(self.xaa_ec_point4_desc if self.xaa_ec_point4_desc else "Write one or two paragraphs describing your point 4.")+"""</p>
                            </div>
                        </div>
                        """
        if self.xaa_ec_point5_icon and self.xaa_ec_point5_title and self.xaa_ec_point5_desc:
            desc_text += """
                        <div class="row">
                            <div style="width:10%;" class="o_colored_level">
                                <img id="xaa_ec_point5_icon" 
                                class="img img-fluid mx-auto" 
                                src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_point5_icon" 
                                loading="lazy">
                            </div>
                            <div style="width:80%;margin:6px;" class="o_colored_level">
                                <p style="margin: auto; font-size: 16px;"><b>
                                """+str(self.xaa_ec_point5_title if self.xaa_ec_point5_title else "A Point 5 Title")+"""</b></p>
                                <p style="font-size: 14px;">
                                """+str(self.xaa_ec_point5_desc if self.xaa_ec_point5_desc else "Write one or two paragraphs describing your point 5.")+"""</p>
                            </div>
                        </div>
                    """
        desc_text += """
                    </div>
                </div>
                <div class="pt16 pb16 col-lg-7 o_colored_level">
                    <img id="xaa_ec_product_image" 
                    class="img img-fluid mx-auto" 
                    src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_product_image" 
                    loading="lazy">
                """
        if self.xaa_ec_product_image_opt:
            desc_text += """
                    <img id="xaa_ec_product_image_opt" 
                    class="img img-fluid mx-auto" 
                    src="/web/image/product.template/"""+str(self.id)+"""/xaa_ec_product_image_opt" 
                    loading="lazy">
                    """
        desc_text += """
                </div>
            </div>
        </div>
        </section>
        """

        return Markup(desc_text)

    @api.constrains('xaa_ec_desciption','xaa_ec_logo','xaa_ec_product_image',
        'xaa_ec_product_image_opt','xaa_ec_point1_icon','xaa_ec_point1_title',
        'xaa_ec_point1_desc','xaa_ec_point2_icon','xaa_ec_point2_title',
        'xaa_ec_point2_desc','xaa_ec_point3_icon','xaa_ec_point3_title',
        'xaa_ec_point3_desc','xaa_ec_point4_icon','xaa_ec_point4_title',
        'xaa_ec_point4_desc','xaa_ec_point5_icon','xaa_ec_point5_title',
        'xaa_ec_point5_desc','name')
    def set_website_product_description(self):
        if self.xaa_ec_desciption == 'automatic':
            if not self.website_description:
                self.website_description = self._set_website_snippet_description()
            elif 'Logo - Text - Icon' not in self.website_description:
                self.website_description += self._set_website_snippet_description()
            else:
                soup = BeautifulSoup(self.website_description, 'html.parser')
                soup.find('section', attrs={"class":"s_text_image"}).extract()
                self.website_description = soup
                self.website_description += self._set_website_snippet_description()
