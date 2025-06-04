from odoo import api, fields, models
from odoo.exceptions import UserError
from .. import api_call  

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # def action_confirm(self):
    #     res = super().action_confirm()  

    #     for order in self:
    #         if order.woo_order_id:
                
    #             api_call.update_order_status(order.woo_order_id, "processing")
    #         # picking = self.env['stock.picking'].search([('origin', '=', order.name)])
    #         # if picking:
    #         #     picking._compute_woo_status()

    #     return res

    def create(self, vals):
        res = super().create(vals)
        for rec in res:
            if rec.name:
                rec.woo_order_id = rec.name
        return res
    
    
    # def write(self, vals):
    #     # res = 
    #     if self.woo_status:
    #         if self.woo_status == "processing":
    #             api_call.update_order_status(self.woo_order_id, "processing")

    #         elif self.woo_status == "220perparation_":
    #             api_call.update_order_status(self.woo_order_id, "220perparation_")
    #         elif self.woo_status == "ready_to_send":
    #             api_call.update_order_status(self.woo_order_id, "ready_to_send")
    #         elif self.woo_status == "776incompleteor":
    #             api_call.update_order_status(self.woo_order_id, "776incompleteor")
    #         elif self.woo_status == "complete":
    #             api_call.update_order_status(self.woo_order_id, "complete")
    #     return super().write(vals)
    
