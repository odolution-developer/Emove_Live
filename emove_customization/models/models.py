from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from odoo.addons.test_convert.tests.test_env import record


class StockWarehouseOrderPointInherit(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    sku = fields.Char(string="SKU", related="product_id.default_code", store=True, readonly=True)
    ean = fields.Char(string="EAN", related="product_id.barcode", store=True, readonly=True)
    hscode = fields.Char(string="HS Code", related="product_id.hs_code", store=True, readonly=True)
    barcode = fields.Char(string="Barcode", related="product_id.barcode", store=True, readonly=True)
    weight = fields.Float(string="Weight", related="product_id.weight", store=True, readonly=True)
    product_image = fields.Binary(string="Product Image", related="product_id.image_1920",store=True)
    product_category = fields.Many2one("product.category", string="Product Category", related="product_id.categ_id", store=True, readonly=True)
    cost = fields.Float(string="Cost", related="product_id.standard_price", store=True, readonly=True)
    sale_price = fields.Float(string="Sale Price", related="product_id.list_price", store=True, readonly=True)

    sales_last_90_days = fields.Integer(string="Last 90 Days",related="product_id.sales_last_90_days",store=True)
    sales_forecast_next_90_days = fields.Integer(string="Next 90 Days",related="product_id.sales_forecast_next_90_days",store=True)
    gross_stock_left = fields.Integer(string="Gross Stock Days Left",related="product_id.gross_stock_left",store=True)


