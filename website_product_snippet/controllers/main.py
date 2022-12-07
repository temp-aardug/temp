# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import http
from odoo.http import request

class ProductSnippet(http.Controller):
    @http.route(['/product/snippet/dynamic_value'], type='json', auth="public", website=True, csrf=False)
    def get_productsnippet_dynamic_value(self, product_id):
        product = request.env['product.template'].sudo().browse(product_id)
        data = {}
        if product:
            data.update({
                'product_id': product.id,
                'xaa_ec_logo': product.xaa_ec_logo,
                'xaa_ec_name': product.name,
                'xaa_ec_product_image': product.xaa_ec_product_image,
                'xaa_ec_product_image_opt': product.xaa_ec_product_image_opt,
                'xaa_ec_point1_icon': product.xaa_ec_point1_icon,
                'xaa_ec_point1_title': product.xaa_ec_point1_title,
                'xaa_ec_point1_desc': product.xaa_ec_point1_desc,
                'xaa_ec_point2_icon': product.xaa_ec_point2_icon,
                'xaa_ec_point2_title': product.xaa_ec_point2_title,
                'xaa_ec_point2_desc': product.xaa_ec_point2_desc,
                'xaa_ec_point3_icon': product.xaa_ec_point3_icon,
                'xaa_ec_point3_title': product.xaa_ec_point3_title,
                'xaa_ec_point3_desc': product.xaa_ec_point3_desc,
                'xaa_ec_point4_icon': product.xaa_ec_point4_icon,
                'xaa_ec_point4_title': product.xaa_ec_point4_title,
                'xaa_ec_point4_desc': product.xaa_ec_point4_desc,
                'xaa_ec_point5_icon': product.xaa_ec_point5_icon,
                'xaa_ec_point5_title': product.xaa_ec_point5_title,
                'xaa_ec_point5_desc': product.xaa_ec_point5_desc
            })
            return data
        else:
            data.update({'product_id': False})
            return data
