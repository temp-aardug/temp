# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import os
import re
import base64
import tempfile
from contextlib import closing
from PyPDF2 import PdfFileWriter, PdfFileReader
from logging import getLogger
from odoo import api, models
from odoo.addons.quote_print.caretutils import listutils

_logger = getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _render_qweb_html(self, report_ref, docids, data=None):
        html = super(IrActionsReport, self)._render_qweb_html(report_ref,
            docids, data=data)
        if (self.model != 'sale.order' and
            self.report_name != 'quote_print.report_web_quotation_custom'):
            return html

        variables = re.findall(b'\${custom:.*?}', html[0])
        if not variables:
            return html
        lst = list(html)
        for i, variChunk in enumerate(listutils.chunks(variables,
            len(variables) / len(docids))):
            for variable in variChunk:
                value = eval(variable[9:-1])
                if isinstance(value, (int, float, list, tuple, dict)):
                    try:
                        '''There are uncertain possible data. So making generic
                        and ignore issue.'''
                        try:
                            value = str(value).encode("utf-8").decode("utf-8")
                        except:
                            value = str(value).decode("utf-8")
                    except:
                        value = u''
                lst[0] = lst[0].replace(variable, value.encode('utf-8'), 1)
        return tuple(lst)

    def _merge_pdf(self, documents):
        """Merge PDF files into one."""
        writer = PdfFileWriter()
        streams = []
        try:
            for document in documents:
                pdfreport = open(document, 'rb')
                streams.append(pdfreport)
                reader = PdfFileReader(pdfreport)
                for page in range(0, reader.getNumPages()):
                    writer.addPage(reader.getPage(page))

            merged_file_fd, merged_file_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.merged.tmp.')
            with closing(os.fdopen(merged_file_fd, 'wb')) as merged_file:
                writer.write(merged_file)
        finally:
            for stream in streams:
                try:
                    stream.close()
                except Exception:
                    pass
        return merged_file_path

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """This method generates and returns pdf version with background of a
           report."""
        
        report_sudo = self._get_report(report_ref)
        self = report_sudo
        temporary_files = []
        pdf = super(IrActionsReport, self)._render_qweb_pdf(report_ref,
            res_ids, data=data)
        if (self.model != 'sale.order' and
            self.report_name != 'quote_print.custom_web_quote_print'):
            return pdf
        soId = res_ids[0] if isinstance(res_ids, list) else res_ids
        so = self.env['sale.order'].browse(soId)
        if not so.sale_order_template_id:
            return pdf
        if so.sale_order_template_id.xaa_aa_isfooteradrsimg_first_page:
            self.paperformat_id.sudo().write({'margin_bottom': 23})
        else:
            self.paperformat_id.sudo().write({'margin_bottom': 35})

        cover_image = so.sale_order_template_id.xaa_aa_cover_image
        cover_image_pdf = so.sale_order_template_id.xaa_aa_cover_image_pdf
        if (cover_image and cover_image_pdf and
            (not so.sale_order_template_id.xaa_aa_report_layout
            or so.sale_order_template_id.xaa_aa_report_layout in
            ['address_only','no_extra_space'])):
            streams = []
            try:
                report_fd, report_path = tempfile.mkstemp(
                    suffix='.pdf', prefix='report.tmp.')
                temporary_files.append(report_path)
                with closing(os.fdopen(report_fd, 'wb')) as repo:
                    repo.write(pdf[0])
            finally:
                for stream in streams:
                    try:
                        stream.close()
                    except Exception:
                        pass

            cover_image_pdf = base64.decodebytes(cover_image_pdf)
            cover_fd, cover_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.tmp.')
            temporary_files.append(cover_path)
            with closing(os.fdopen(cover_fd, 'wb')) as repo:
                repo.write(cover_image_pdf)

            mergeFile = self._merge_pdf([cover_path, report_path])
            with open(mergeFile, 'rb') as pdfdocument:
                pdf = pdfdocument.read(), 'pdf'

        close_image = so.sale_order_template_id.xaa_aa_close_image
        close_image_pdf = so.sale_order_template_id.xaa_aa_close_image_pdf
        if close_image and close_image_pdf:
            streams = []
            try:
                report_fd, report_path = tempfile.mkstemp(
                    suffix='.pdf', prefix='report.tmp.')
                temporary_files.append(report_path)
                with closing(os.fdopen(report_fd, 'wb')) as repo:
                    repo.write(pdf[0])
            finally:
                for stream in streams:
                    try:
                        stream.close()
                    except Exception:
                        pass

            close_image_pdf = base64.decodebytes(close_image_pdf)
            close_fd, close_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.tmp.')
            temporary_files.append(close_path)
            with closing(os.fdopen(close_fd, 'wb')) as repo:
                repo.write(close_image_pdf)

            mergeFile = self._merge_pdf([report_path, close_path])
            with open(mergeFile, 'rb') as pdfdocument:
                pdf = pdfdocument.read(), 'pdf'

        # Manual cleanup of the temporary files
        for temporary_file in temporary_files:
            try:
                os.unlink(temporary_file)
            except (OSError, IOError):
                _logger.error('Error when trying to remove file %s' % temporary_file)

        return pdf

    @api.model
    def _run_wkhtmltopdf(
            self,
            bodies,
            report_ref=False,
            header=None,
            footer=None,
            landscape=False,
            specific_paperformat_args=None,
            set_viewport_size=False):

        if self.report_name == 'quote_print.custom_web_quote_print':
            set_viewport_size = True
        res = super(IrActionsReport, self)\
            ._run_wkhtmltopdf(
                bodies,
                report_ref,
                header,
                footer,
                landscape,
                specific_paperformat_args=specific_paperformat_args,
                set_viewport_size=set_viewport_size
            )
        return res
