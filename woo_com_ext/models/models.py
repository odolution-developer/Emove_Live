# -*- coding: utf-8 -*-

from odoo import models, api, fields


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    proof_payment = fields.Binary(string="Justificante de pago")
    seguimient = fields.Char(string="Seguimient")
    country_code = fields.Char(string="País",realted="partner_id.country_code")

class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    proof_payment = fields.Binary(related="sale_id.proof_payment",string="Justificante de pago")
    seguimient = fields.Char(related="sale_id.seguimient",string="Seguimient")
    country_code = fields.Char(related="sale_id.country_code",string="País",realted="partner_id.country_code")
    date_order = fields.Datetime(related="sale_id.date_order",string="País",realted="partner_id.country_code")
    woo_status = fields.Selection([("pending", "Pending"), ("processing", "Processing"),
                                   ("on-hold", "On hold"), ("completed", "Completed"),
                                   ("cancelled", "Cancelled"), ("refunded", "Refunded"),
                                    ("enviado", "Madrid"),("252completadopa", "Valencia"),
                                    ("100recogidaalma", "Recogida almacén"),
                                    ("169pendientedec", "Pendiente de cobro (Enviado)"),
                                    ("completed", "Completado"),("237recogidavale", "Recogidavale"),("enviado", "enviado"),("refunded", "Refunded")], related="sale_id.woo_status")
    payment_gateway_id = fields.Many2one("woo.payment.gateway", "Woo Payment Gateway",related="sale_id.payment_gateway_id")
    amount_total = fields.Monetary(
        related='sale_id.amount_total',
        string='Sale Order Total',
        currency_field='company_currency_id',  # or 'currency_id' depending on your setup
        store=True  # Optional: Store in the database for faster access
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        readonly=True
    )
    woo_coupon_ids = fields.Many2many("woo.coupons.ept", string="Coupons",related="sale_id.woo_coupon_ids")
    woo_order_id = fields.Char("Woo Order Reference",related="sale_id.woo_order_id")





class WooOrderInh(models.Model):
    _inherit = 'woo.order.data.queue.line.ept'

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        for rec in record:
            try:
                rec.auto_order_queue_lines_process()
            except:
                pass
        return record

class WooProductInh(models.Model):
    _inherit = 'woo.product.data.queue.line.ept'

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        for rec in record:
            try:
                rec.sync_woo_product_data()
            except:
                pass
        return record

class WooCustomerInh(models.Model):
    _inherit = 'woo.customer.data.queue.line.ept'

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        for rec in record:
            try:
                rec.woo_customer_data_queue_to_odoo()
            except:
                pass
        return record

class WooExportStockInh(models.Model):
    _inherit = 'woo.export.stock.queue.line.ept'

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        for rec in record:
            try:
                rec.auto_export_stock_queue_lines_process()
            except:
                pass
        return record


class WooProductProductEptInh(models.Model):
    _inherit = 'woo.product.product.ept'

    def write(self, vals):
        rec = super().write(vals)
        if 'name' in vals:
            self.product_id.name = self.name
        if 'default_code' in vals:
            self.product_id.default_code = self.default_code
        return rec

class WooProductTemplateEptInh(models.Model):
    _inherit = 'woo.product.template.ept'

    def write(self, vals):
        rec = super().write(vals)

        if 'name' in vals:
            self.product_tmpl_id.name = self.name
        if 'default_code' in vals:
            self.product_tmpl_id.default_code = self.default_code
        if 'woo_description' in vals:
            self.product_tmpl_id.description_sale = self.woo_description
        if 'woo_short_description' in vals:
            self.product_tmpl_id.description_sale = self.woo_description

        return rec
