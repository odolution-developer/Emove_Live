from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    sales_last_90_days = fields.Integer(string="Last 90 Days", compute="compute_next_90_days", store=True)
    sales_forecast_next_90_days = fields.Integer(string="Next 90 Days", compute="compute_next_90_days",
                                                 store=True)
    gross_stock_left = fields.Integer(string="Gross Stock Days Left", compute="compute_next_90_days", store=True)

    @api.depends("company_id","qty_available")
    def compute_next_90_days(self):
        today = date.today().replace(day=1)
        till_date = (today + relativedelta(months=3)).replace(day=1)
        for record in self:
            start_date = today - timedelta(days=90)
            sales_count = sum(self.env['sale.order.line'].search([('product_id', '=', record.product_variant_id.id), ('order_id.state', 'not in', ['cancel']),
                 ('order_id.date_order', '>=', start_date)
                 ]).mapped('product_uom_qty'))
            record.sales_last_90_days = sales_count
            sales_prediction = 0
            for line in record.product_variant_id.prediction_lines:
                if line.actual_date > today and line.actual_date <= till_date:
                    sales_prediction += line.sales_prediction
            record.sales_forecast_next_90_days = sales_prediction
            every_day = (record.sales_last_90_days / 90)
            record.gross_stock_left = (record.qty_available /every_day) if every_day else 0



class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    sales_last_90_days = fields.Integer(string="Last 90 Days", compute="compute_next_90_days", store=True)
    sales_forecast_next_90_days = fields.Integer(string="Next 90 Days", compute="compute_next_90_days", store=True)
    gross_stock_left = fields.Integer(string="Gross Stock Days Left", compute="compute_next_90_days", store=True)

    @api.depends("company_id","qty_available")
    def compute_next_90_days(self):
        today = date.today().replace(day=1)
        till_date = (today + relativedelta(months=3)).replace(day=1)
        for record in self:
            start_date = today - timedelta(days=90)
            sales_count = sum(self.env['sale.order.line'].search(
                [('product_id', '=', record.id), ('order_id.state', 'not in', ['cancel']),
                 ('order_id.date_order', '>=', start_date)
                 ]).mapped('product_uom_qty'))
            record.sales_last_90_days = sales_count
            sales_prediction = 0
            for line in record.prediction_lines:
                if line.actual_date > today and line.actual_date <= till_date:
                    sales_prediction += line.sales_prediction
            record.sales_forecast_next_90_days = sales_prediction
            every_day = (record.sales_last_90_days / 90)
            print(every_day)
            record.gross_stock_left = (record.qty_available /every_day) if every_day else 0

