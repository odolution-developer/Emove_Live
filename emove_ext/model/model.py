# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import xmlrpc.client
import xmlrpc.client
from os.path import dirname, abspath
import csv
import requests
import logging
from odoo import models, fields, api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import file_open
import base64
import requests
from io import BytesIO
from PIL import Image
import base64
from odoo.exceptions import ValidationError

class ProductInh(models.Model):
    _inherit = 'product.product'

    def _check_duplicated_product_barcodes(self, barcodes_within_company, company_id):
        pass





class ProductInh(models.Model):
    _inherit = 'product.template'

    def import_file(self):
        CSV_URL = "https://emovedistribution.com/wp-content/uploads/woo-feed/custom/csv/odoo.csv"
        response = requests.get(CSV_URL, timeout=10)
        response.raise_for_status()
        decoded_content = response.content.decode("utf-8")
        csv_reader = csv.DictReader(decoded_content.splitlines())
        for row in csv_reader:
            if row.get("id"):
                woo_product = self.env["woo.product.product.ept"].search([("variant_id", "=", row.get("id"))], limit=1)
                existing_product = self.env["product.product"].search([("id", "=", woo_product.product_id.id)], limit=1)
                if existing_product:
                    barcode_product = self.env["product.product"].search([("barcode", "=", row.get("ean"))],limit=1)
                    if barcode_product:
                        product_vals = {
                            "name": row.get("title"),
                            "default_code": row.get("sku"),
                        }
                        existing_product.write(product_vals)
                        _logger.info(f"Updated Product: {row.get('sku')}")
                    else:
                        if row.get("ean") != 'New':
                            product_vals = {
                                "name": row.get("title"),
                                "default_code": row.get("sku"),
                                "barcode": row.get("ean"),
                            }
                            existing_product.write(product_vals)
                    # if existing_product.qty_available != row.get("quantity"):
                    #     self.env['stock.change.product.qty'].create({
                    #         'product_id': existing_product.id,
                    #         'product_tmpl_id': existing_product.product_tmpl_id.id,
                    #         'new_quantity': row.get("quantity"),
                    #     }).change_product_qty()
