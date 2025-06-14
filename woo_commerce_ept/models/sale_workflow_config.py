# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class WooSaleAutoWorkflowConfiguration(models.Model):
    _name = "woo.sale.auto.workflow.configuration"
    _description = "WooCommerce Financial Status"

    woo_financial_status = fields.Selection([('paid', 'The finances have been paid'),
                                             ('not_paid', 'The finances have been not paid')],
                                            default="paid", required=True, string="WooCommerce Financial Status")
    woo_auto_workflow_id = fields.Many2one("sale.workflow.process.ept", "Auto Workflow", required=True)
    woo_instance_id = fields.Many2one("woo.instance.ept", "Instance", required=True)
    woo_payment_gateway_id = fields.Many2one("woo.payment.gateway", "Payment Gateway", required=True)
    active = fields.Boolean(default=True)
    woo_order_status = fields.Selection([("processing", "Processing"),
                                         ("pending", "Pending Payment"),
                                         ("on-hold", "On hold"),
                                         ("completed", "Completed"),
                                         ("cancelled", "Cancelled"),
                                        ("enviado", "Madrid"),
                                         ("252completadopa", "Valencia"),("237recogidavale", "Recogidavale"),("100recogidaalma", "Recogida almacén"),
                                         ("169pendientedec", "Pendiente de cobro (Enviado)"),("enviado", "enviado"),("completed", "Completado"),("refunded", "Refunded")],
                                        default="processing")

    _sql_constraints = [
        ('_workflow_unique_constraint',
         'unique(woo_financial_status,woo_instance_id,woo_payment_gateway_id,woo_order_status)',
         'Financial status must be unique in the list')]
