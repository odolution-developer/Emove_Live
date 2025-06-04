# -*- coding: utf-8 -*-
import base64
from os.path import abspath, dirname

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.tools import format_amount


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    image_128 = fields.Image(string="Image",related="product_id.image_128",store=True)


class PurchaseExtInh(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('on_hold', 'On Hold'),
        ('processing', 'Processing'),
        ('purchase', 'On The Way'),
        ('done', 'On The Way'),('arrived', 'Arrived'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    sent_by = fields.Selection([
        ('ship', 'Ship'),
        ('plane', 'Plane'),
    ], string='Sent by',copy=False)
    image = fields.Binary(string='Image', compute='_compute_image', store=False)

    @api.depends('sent_by')
    def _compute_image(self):
        for record in self:
            image_map = {
                'ship': '/emove_customization/static/description/ship.jpeg',
            'plane': '/emove_customization/static/description/plan.jpeg',
            }
            image_path = image_map.get(record.sent_by)
            record.image = self._get_image_binary(image_path) if image_path else False

    def _get_image_binary(self, image_path):
        """
        Reads an image file from the static folder and converts it to base64.
        """
        try:
            # Get the absolute path of the image
            path = abspath(dirname(dirname(dirname(__file__)))) + image_path
            with open(path, 'rb') as image_file:
                return base64.b64encode(image_file.read())
        except FileNotFoundError:
            return False

    def action_delivery_validate(self):
        for picking in self.picking_ids.filtered(lambda rec: rec.state not in ['done', 'cancel']):
            picking.button_validate()
        self.state='arrived'

    def action_set_on_hold(self):
        self.state = "on_hold"

    def action_set_processing(self):
        self.state = "processing"


    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'processing']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
            order.button_done()
        self.create_price_list()
        return True

    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the purchase order views.
        """
        self.check_access_rights('read')

        result = {
            'all_to_send': 0,
            'all_waiting': 0,
            'all_late': 0,
            'my_to_send': 0,
            'my_waiting': 0,
            'my_late': 0,
            'all_avg_order_value': 0,
            'all_avg_days_to_purchase': 0,
            'all_total_last_7_days': 0,
            'all_sent_rfqs': 0,
            'all_arrived': 0,  # Add for arrived orders
            'company_currency_symbol': self.env.company.currency_id.symbol
        }

        one_week_ago = fields.Datetime.to_string(fields.Datetime.now() - relativedelta(days=7))

        query = """SELECT COUNT(1)
                       FROM mail_message m
                       JOIN purchase_order po ON (po.id = m.res_id)
                       WHERE m.create_date >= %s
                         AND m.model = 'purchase.order'
                         AND m.message_type = 'notification'
                         AND m.subtype_id = %s
                         AND po.company_id = %s;
                    """

        self.env.cr.execute(query, (one_week_ago, self.env.ref('purchase.mt_rfq_sent').id, self.env.company.id))
        res = self.env.cr.fetchone()
        result['all_sent_rfqs'] = res[0] or 0

        # easy counts
        po = self.env['purchase.order']

        result['all_onhold'] = po.search_count([('state', '=', 'on_hold')])
        result['all_processing'] = po.search_count([('state', '=', 'processing')])
        result['all_onway'] = po.search_count([('state', '=', ['done','purchase'])])
        result['all_arrived'] = po.search_count([('state', '=', 'arrived')])  # Add arrived orders count

        result['all_to_send'] = po.search_count([('state', '=', 'draft')])
        result['my_to_send'] = po.search_count([('state', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['all_waiting'] = po.search_count([('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now())])
        result['my_waiting'] = po.search_count(
            [('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now()), ('user_id', '=', self.env.uid)])
        result['all_late'] = po.search_count(
            [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now())])
        result['my_late'] = po.search_count(
            [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now()),
             ('user_id', '=', self.env.uid)])


        # Calculated values ('avg order value', 'avg days to purchase', and 'total last 7 days') note that 'avg order value' and
        # 'total last 7 days' takes into account exchange rate and current company's currency's precision.
        # This is done via SQL for scalability reasons
        query = """SELECT AVG(COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total)),
                              AVG(extract(epoch from age(po.date_approve,po.create_date)/(24*60*60)::decimal(16,2))),
                              SUM(CASE WHEN po.date_approve >= %s THEN COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total) ELSE 0 END)
                       FROM purchase_order po
                       WHERE po.state in ('purchase', 'done')
                         AND po.company_id = %s
                    """
        self._cr.execute(query, (one_week_ago, self.env.company.id))
        res = self.env.cr.fetchone()
        result['all_avg_days_to_purchase'] = round(res[1] or 0, 2)
        currency = self.env.company.currency_id
        result['all_avg_order_value'] = format_amount(self.env, res[0] or 0, currency)
        result['all_total_last_7_days'] = format_amount(self.env, res[2] or 0, currency)

        return result

    def create_price_list(self):
        for line in self.order_line:
            product_supplier = self.env['product.supplierinfo'].search(
                [('partner_id', '=', self.partner_id.id), ('product_id', '=', line.product_id.id)], limit=1)
            if not product_supplier:
                # Create new supplier info
                r = self.env['product.supplierinfo'].create({
                    'product_id': line.product_id.id,
                    'product_tmpl_id': line.product_id.product_tmpl_id.id,
                    'partner_id': self.partner_id.id,
                    'price': line.price_unit,
                    'min_qty': 1,
                    'delay': 1,
                })
            else:
                # Update the supplier price
                product_supplier.price = line.price_unit

            # Multiply the standard price by 1.25
            line.product_id.standard_price = line.product_id.standard_price * 1.25
