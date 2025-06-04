import base64
import datetime
import io
import zipfile
from collections import defaultdict
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from deep_translator import GoogleTranslator

class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    def action_print_quantity_labels(self):
        report_template = 'product_label_custom.report_product_label_25x37'
        attachments = []

        for order in self:
            for line in order.order_line:
                print(order.name)
                report_content, report_format = self.env['ir.actions.report']._render_qweb_pdf(
                                report_template, [line.product_id.id for _ in range(int(line.product_qty))] )
                print(report_content)
                pdf_base64 = base64.b64encode(report_content)
                attachment = self.env['ir.attachment'].create({
                    'name': f'{order.name}.pdf',
                    'type': 'binary',
                    'datas': pdf_base64,
                    'res_model': 'product.product',
                    'res_id': line.product_id.id,
                    'mimetype': 'application/pdf'
                })
                attachments.append(attachment)
                # attachments.append({
                #     "attachment": attachment,
                #     # "qty": line.product_qty,
                #     "po_name": line.order_id.name,
                # })
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for attachment in attachments:
                # for qty in range(0, int(attachment.get('qty'))):
                pdf_data = base64.b64decode(attachment.datas)
                zip_file.writestr(attachment.name, pdf_data)

        zip_buffer.seek(0)
        zip_data = zip_buffer.read()
        zip_base64 = base64.b64encode(zip_data)

        zip_attachment = self.env['ir.attachment'].create({
            'name': 'Purchase_orders_labels.zip',
            'type': 'binary',
            'datas': zip_base64,
            'res_model': 'purchase.order',
            'res_id': self[0].id,
            'mimetype': 'application/zip'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{zip_attachment.id}?download=true',
            'target': 'self',
        }

    def action_print_labels(self):
        report_template = 'product_label_custom.report_product_label_25x37'
        attachments = []

        for order in self:
            for line in order.order_line:
                print(order.name)
                report_content, report_format = self.env['ir.actions.report']._render_qweb_pdf(
                                report_template, [line.product_id.id])
                print(report_content)
                pdf_base64 = base64.b64encode(report_content)
                attachment = self.env['ir.attachment'].create({
                    'name': f'{line.product_id.default_code}.pdf',
                    'type': 'binary',
                    'datas': pdf_base64,
                    'res_model': 'product.product',
                    'res_id': line.product_id.id,
                    'mimetype': 'application/pdf'
                })
                attachments.append(attachment)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for attachment in attachments:
                pdf_data = base64.b64decode(attachment.datas)
                zip_file.writestr(attachment.name, pdf_data)

        zip_buffer.seek(0)
        zip_data = zip_buffer.read()
        zip_base64 = base64.b64encode(zip_data)

        zip_attachment = self.env['ir.attachment'].create({
            'name': 'Purchase_orders_labels.zip',
            'type': 'binary',
            'datas': zip_base64,
            'res_model': 'purchase.order',
            'res_id': self[0].id,
            'mimetype': 'application/zip'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{zip_attachment.id}?download=true',
            'target': 'self',
        }

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('patient_default_code', 'unique(default_code)', 'Internal Reference  must be unique !'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if not vals.get('barcode'):
                seq_date = None
                if 'company_id' in vals:
                    vals['barcode'] = self.env['ir.sequence'].with_context(
                        force_company=vals['company_id']).next_by_code(
                        'product.template', sequence_date=seq_date) or _('New')
                else:
                    vals['barcode'] = self.env['ir.sequence'].next_by_code(
                        'product.template', sequence_date=seq_date) or _('New')
                related_vals['barcode'] = vals['barcode']
            if related_vals:
                template.write(related_vals)
        return templates


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('patient_default_code', 'unique(default_code)', 'Internal Reference  must be unique !'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        for product, vals in zip(products, vals_list):
            related_vals = {}
            if not vals.get('barcode'):
                seq_date = None
                if 'company_id' in vals:
                    vals['barcode'] = self.env['ir.sequence'].with_context(
                        force_company=vals['company_id']).next_by_code(
                        'product.product', sequence_date=seq_date) or _('New')
                else:
                    vals['barcode'] = self.env['ir.sequence'].next_by_code(
                        'product.product', sequence_date=seq_date) or _('New')
                related_vals['barcode'] = vals['barcode']
                if related_vals:
                    product.write(related_vals)
        return products

    def get_translated_name(self, name):
        try:
            translated_phrase = GoogleTranslator(source='es', target='en').translate(name)
            return translated_phrase
        except Exception as e:
            return name


