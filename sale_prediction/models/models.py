# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import math
import logging
from datetime import date, timedelta
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class stockwarehouseInh(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.depends('qty_multiple', 'qty_forecast', 'product_min_qty', 'product_max_qty', 'visibility_days')
    def _compute_qty_to_order(self):
        for orderpoint in self:
            if not orderpoint.product_id or not orderpoint.location_id:
                orderpoint.qty_to_order = False
                continue
            qty_to_order = 0.0
            rounding = orderpoint.product_uom.rounding
            # We want to know how much we should order to also satisfy the needs that gonna appear in the next (visibility) days
            product_context = orderpoint._get_product_context(visibility_days=orderpoint.visibility_days)
            qty_forecast_with_visibility = \
            orderpoint.product_id.with_context(product_context).read(['virtual_available'])[0]['virtual_available'] + \
            orderpoint._quantity_in_progress()[orderpoint.id]
            if float_compare(qty_forecast_with_visibility, orderpoint.product_min_qty, precision_rounding=rounding) < 0:
                qty_to_order = max(orderpoint.product_min_qty,
                                   orderpoint.product_max_qty) - qty_forecast_with_visibility
                remainder = orderpoint.qty_multiple > 0.0 and qty_to_order % orderpoint.qty_multiple or 0.0
                if (float_compare(remainder, 0.0, precision_rounding=rounding) > 0
                        and float_compare(orderpoint.qty_multiple - remainder, 0.0, precision_rounding=rounding) > 0):
                    qty_to_order += orderpoint.qty_multiple - remainder
            prediction_line = self.env['product.prediction.line'].search(
                [('product_id', '=', orderpoint.product_id.id)]).filtered(lambda
                                                                              i: i.actual_date.month == datetime.today().date().month and i.actual_date.year == datetime.today().date().year)

            if orderpoint.product_id.is_manual == True:
                if orderpoint.product_id.qty_available >= orderpoint.product_min_qty:
                   qty_to_order = 0
            if prediction_line and prediction_line.min_qty > 0:
                if orderpoint.product_id.is_manual == False:
                    orderpoint.product_min_qty = prediction_line.min_qty
                    if orderpoint.product_id.qty_available < prediction_line.min_qty:
                        qty_to_order = prediction_line.to_order_value
                    else:
                        qty_to_order = 0
            orderpoint.qty_to_order = qty_to_order


class ProductProductInh(models.Model):
    _inherit = 'product.product'

    value = fields.Integer()
    prediction_lines = fields.One2many('product.prediction.line', 'product_id')
    publish_date = fields.Date()
    case = fields.Char()
    is_manual = fields.Boolean(string="Manual")

    def action_predict_greater_than_two_years(self):
        self.case = "2"
        woo_product_obj = self.env['sale.order.line']
        publish_date = woo_product_obj.sudo().search([('product_id', '=', self.id)], order='date_order asc',
                                                     limit=1).order_id.date_order.date()
        _logger.info('Publish date 2 : %s', publish_date)
        sales = self.env['sale.order.line'].sudo().search(
            [('product_id', '=', self.id), ('order_id.state', 'not in', ["cancel"])]).filtered(lambda
                                                                                                   i: i.order_id.date_order.date() >= publish_date and i.order_id.date_order.date() <= datetime.today().date())
        check = True
        new_date = publish_date
        self.prediction_lines.unlink()
        sales_list = []
        prediction_list = []
        predict_record = False
        while check:
            if new_date > datetime.today().date():
                check = False
            else:
                sale = sum(sales.filtered(lambda
                                              j: j.order_id.date_order.date().month == new_date.month and j.order_id.date_order.date().year == new_date.year).mapped(
                    'product_uom_qty'))
                val = {
                    'actual_date': new_date.replace(day=1),
                    'date': str(new_date.year) + "-" + str(new_date.month),
                    'sales': sale,
                    'product_id': self.id,
                }
                predict_record = self.env['product.prediction.line'].create(val)
                sales_list.append(val)
                new_date = new_date + relativedelta(months=1)
        if predict_record:
            today = date.today().replace(day=1)
            from_date = today - relativedelta(months=1)
            till_date = today - relativedelta(years=1)
            old_date = till_date - relativedelta(years=1)
            last_year_month_date = today - relativedelta(years=1)

            sale_predict = [s.get('sales') for s in sales_list if
                            s.get('actual_date') >= till_date and s.get('actual_date') <= from_date and s.get(
                                'sales') > 0]

            sale_predict_before = [s.get('sales') for s in sales_list if
                                   s.get('actual_date') >= old_date and s.get('actual_date') < till_date and s.get(
                                       'sales') > 0]
            lst_year_month_sale = sum([s.get('sales') for s in sales_list if
                                       s.get('actual_date').month == last_year_month_date.month and s.get(
                                           'actual_date').year == last_year_month_date.year and s.get('sales') > 0])
            # print(lst_year_month_sale)
            if sale_predict:
                sale_predict_sum = (sum(sale_predict))
                sale_predict_len = len(sale_predict) or 1
                sale_predict_avg = sale_predict_sum / sale_predict_len
                sale_predict_before_sum = (sum(sale_predict_before))
                sale_predict_before_len = len(sale_predict_before)
                sale_predict_before_avg = sale_predict_before_sum / (sale_predict_before_len or 1)
                lst_year_month_sale = lst_year_month_sale if lst_year_month_sale else sale_predict_before_avg
                value = (sale_predict_avg / (sale_predict_before_avg or 1)) * lst_year_month_sale
                predict_record.sales_prediction = value
                prediction_list.append({
                    'actual_date': predict_record.actual_date,
                    'sales_prediction': value,
                })
        for r in range(1, 7):
            today = date.today()
            nxt_month_date = (today + relativedelta(months=r)).replace(day=1)
            # s_date = (nxt_month_date - relativedelta(months=1)).replace(day=1)
            s_date = nxt_month_date
            end_date = (s_date - relativedelta(months=12)).replace(day=1)
            from_date = (end_date - relativedelta(months=1)).replace(day=1)
            to_date = (end_date - relativedelta(months=12)).replace(day=1)
            last_year_month_date = (s_date - relativedelta(months=12)).replace(day=1)
            sale_predict = [s.get('sales') for s in sales_list if
                            s.get('actual_date') < s_date and s.get('actual_date') >= end_date and s.get('sales') > 0]

            sale_predict_before = [s.get('sales') for s in sales_list if
                                   s.get('actual_date') >= to_date and s.get('actual_date') <= from_date and s.get(
                                       'sales') > 0]

            lst_year_month_sale = sum([s.get('sales') for s in sales_list if
                                       s.get('actual_date').month == last_year_month_date.month and s.get(
                                           'actual_date').year == last_year_month_date.year and s.get('sales') > 0])

            value_avg1 = sum(sale_predict) / (len(sale_predict) or 1)
            value_avg2 = sum(sale_predict_before) / (len(sale_predict_before) or 1)

            lst_year_month_sale = lst_year_month_sale if lst_year_month_sale else value_avg2
            value = (value_avg1 / (value_avg2 or 1)) * lst_year_month_sale
            val = {
                'actual_date': nxt_month_date.replace(day=1),
                'date': str(nxt_month_date.year) + "-" + str(nxt_month_date.month),
                'product_id': self.id,
                'sales_prediction': value,
            }
            predict_record = self.env['product.prediction.line'].create(val)
            prediction_list.append({
                'actual_date': predict_record.actual_date,
                'sales_prediction': value,
            })

        for line in self.prediction_lines:
            if line.sales_prediction:
                min_date = line.actual_date + relativedelta(months=3)
                # print(line.actual_date,min_date)
                min_qty = [s.get('sales_prediction') for s in prediction_list if
                           s.get('actual_date') > line.actual_date and s.get('actual_date') <= min_date]
                # print(min_qty)
                order_date = line.actual_date + relativedelta(months=6)
                order_qty = [s.get('sales_prediction') for s in prediction_list if
                             s.get('actual_date') > line.actual_date + relativedelta(months=3) and s.get(
                                 'actual_date') <= order_date]
                line.min_qty = sum(min_qty)
                line.to_order_value = 50 * math.ceil(sum(order_qty) / 50)

    def action_predict(self):
        woo_product_obj = self.env['sale.order.line']
        sale_line = woo_product_obj.sudo().search([('product_id', '=', self.id)], order='date_order asc', limit=1)
        if sale_line:
            publish_date = sale_line.order_id.date_order.date()
            _logger.info('Publish date : %s', publish_date)
            months = float((datetime.today().date() - publish_date).days / 30.44)
            print("-----", months)
            if months <= 24:
                self.case = "1"
                print("coming if")
                sales = self.env['sale.order.line'].sudo().search(
                    [('product_id', '=', self.id), ('order_id.state', 'not in', ["cancel"])]).filtered(lambda
                                                                                                           i: i.order_id.date_order.date() >= publish_date and i.order_id.date_order.date() <= datetime.today().date())
                check = True
                new_date = publish_date
                self.prediction_lines.unlink()
                sales_list = []
                prediction_list = []
                predict_record = False
                while check:
                    if new_date > datetime.today().date():
                        check = False
                    else:
                        sale = sum(sales.filtered(lambda
                                                      j: j.order_id.date_order.date().month == new_date.month and j.order_id.date_order.date().year == new_date.year).mapped(
                            'product_uom_qty'))
                        val = {
                            'actual_date': new_date,
                            'date': str(new_date.year) + "-" + str(new_date.month),
                            'sales': sale,
                            'product_id': self.id,
                        }
                        predict_record = self.env['product.prediction.line'].create(val)
                        sales_list.append(val)
                        new_date = new_date + relativedelta(months=1)
                if predict_record:
                    sale_predict = [s.get('sales') for s in sales_list if
                                    s.get('actual_date') < new_date and s.get('sales') > 0]
                    if sale_predict:
                        predict_record.sales_prediction = sum(sale_predict) / len(sale_predict)
                        prediction_list.append({
                            'actual_date': predict_record.actual_date,
                            'sales_prediction': sum(sale_predict) / len(sale_predict),
                        })
                for r in range(0, 7):
                    s_date = new_date + relativedelta(months=r)
                    sale_predict = [s.get('sales') for s in sales_list if
                                    s.get('actual_date') < s_date and s.get('sales') > 0]
                    val = {
                        'actual_date': s_date,
                        'date': str(s_date.year) + "-" + str(s_date.month),
                        'product_id': self.id,
                        'sales_prediction': sum(sale_predict) / (len(sale_predict) or 1),
                    }
                    predict_record = self.env['product.prediction.line'].create(val)
                    prediction_list.append({
                        'actual_date': predict_record.actual_date,
                        'sales_prediction': sum(sale_predict) / (len(sale_predict) or 1),
                    })

                for line in self.prediction_lines:
                    if line.sales_prediction:
                        min_qty = [s.get('sales_prediction') for s in prediction_list if
                                   s.get('actual_date') > line.actual_date and s.get(
                                       'actual_date') <= line.actual_date + relativedelta(months=3)]
                        order_qty = [s.get('sales_prediction') for s in prediction_list if
                                     s.get('actual_date') > line.actual_date + relativedelta(months=3) and s.get(
                                         'actual_date') <= line.actual_date + relativedelta(months=6)]
                        line.min_qty = sum(min_qty)
                        line.to_order_value = 50 * math.ceil(sum(order_qty) / 50)


            else:
                self.action_predict_greater_than_two_years()

    def cron_predict_sale_and_reorder(self):
        products = self.env['product.product'].search([('detailed_type', '=', 'product'), ('default_code', '!=', '')])
        for product in products:
            product.action_predict()

    def cron_cal_min_max(self):
        products = self.env['product.product'].search([('detailed_type', '=', 'product'), ('default_code', '!=', '')])
        for product in products.filtered(lambda i: i.default_code):
            prediction_line = self.env['product.prediction.line'].search([('product_id', '=', product.id)]).filtered(
                lambda
                    i: i.actual_date.month == datetime.today().date().month and i.actual_date.year == datetime.today().date().year)
            min_qty = prediction_line.min_qty
            order_qty = prediction_line.to_order_value
            rr = self.env['stock.warehouse.orderpoint'].search([('product_id', '=', product.id)], limit=1)
            if rr:
              if product.qty_available > min_qty:
                    rr = rr.sudo().write({
                        'qty_to_order': 0,
                    })
            else:
                if product.default_code and product.qty_available < min_qty:
                    rr = self.env['stock.warehouse.orderpoint'].create({
                        'name': product.name,
                        'trigger': "manual",
                        'location_id': 8,
                        'product_id': product.id,
                        'product_tmpl_id': product.product_tmpl_id.id,
                        'product_min_qty': min_qty,
                        'qty_multiple': 1,
                        'qty_to_order': order_qty if product.qty_available < min_qty else 0,
                    })


class ProductPrediction(models.Model):
    _name = 'product.prediction.line'

    product_id = fields.Many2one('product.product')
    actual_date = fields.Date()
    date = fields.Char()
    sales = fields.Integer()
    sales_prediction = fields.Integer()
    min_qty = fields.Integer(string="MIN Quantity")
    to_order_value = fields.Integer()
