from odoo import models, fields, api
from odoo.exceptions import UserError

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def update_replenishment_records(self):
        for rec in self :
            prd = rec.product_id
            po_lines = self.env['purchase.order.line'].search([('product_id', '=', prd.id),('order_id.state','in',['draft','sent','to approve','on_hold','processing','purchase','done','arrived'])])
            total_qty = rec.product_id.qty_available
            if po_lines:
                for line in po_lines:
                    if line.order_id.state in ['draft','sent','to approve','on_hold','processing']:
                        total_qty += line.product_qty
                    elif line.order_id.state in ['purchase','done','arrived'] and line.order_id.picking_ids:
                        for picking in line.order_id.picking_ids:
                            if picking.state == 'assigned':
                                total_qty += line.product_qty
                if total_qty >= rec.product_min_qty and total_qty != rec.product_id.qty_available:
                    # raise UserError([total_qty, rec.product_min_qty,rec.product_id.qty_available,rec.product_id.default_code])
                    rec.unlink()





