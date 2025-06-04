
# Multiple Backorder
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from .. import api_call
import logging
import json
import random
import string
from odoo.exceptions import UserError


_logger_ = logging.getLogger(__name__) 


class Generate_coupon(http.Controller):


    @http.route('/generate_coupon',methods=["POST"],type="json",auth="public")
    def get_coupon(self,**kwargs):
        sorted_lines = kwargs.get('sorted_lines')
        # raise UserError("sorted_lines: "+ str(sorted_lines))
        myreturn = []
        already_generated = False
        created_successfully = False
        quantities_scanned = False
        unit_price_not_found = False
        batch_not_found = False
        product_not_found = False
        sale_not_found = False
        picking_not_found = False

        if not sorted_lines:
            return {
                'status':"Error",
                'message':"Stock Line Not Found",
                "req":str(kwargs)
            }
        for rec_line in sorted_lines:
            move_line=request.env['stock.move.line'].browse(int(rec_line['id']))
            if move_line and move_line.batch_id:
                batch_picking = request.env['stock.picking.batch'].browse(move_line.batch_id.id)
                if batch_picking and batch_picking.picking_ids:
                    for picking_id in batch_picking.picking_ids:
                        picking = request.env['stock.picking'].browse(picking_id.id)
                        if picking:
                            sale = request.env['sale.order'].browse(picking.sale_id.id)
                            if sale:
                                for line in sale.order_line:
                                    if line.product_id.id == move_line.product_id.id:
                                        if move_line.quantity and line.price_unit:
                                            if line.product_uom_qty > rec_line['qty_done']:
                                                random_alphabet = ''.join(random.choices(string.ascii_uppercase, k=3))
                                                coupon_code = random_alphabet + "-" + sale.name
                                                code = api_call.create_coupon(coupon_code, line.price_unit, move_line.quantity)
                                                picking.coupon_code = code
                                                created_successfully = True
                                            else:
                                                quantities_scanned = True
                                        else:
                                            unit_price_not_found = True
                                    else:
                                        product_not_found = True

                            else:
                                sale_not_found = True 
                        else:
                            picking_not_found = True 
            # elif move_line and move_line.picking_id:
            #     picking = request.env['stock.picking'].browse(move_line.picking_id.id)
            #     if picking:
            #         sale = request.env['sale.order'].browse(picking.sale_id.id)
            #         if sale:
            #             for line in sale.order_line:
            #                 if line.product_id.id == move_line.product_id.id:
            #                     if move_line.quantity and line.price_unit:
            #                         if line.product_uom_qty > rec_line['qty_done']:
            #                             random_alphabet = ''.join(random.choices(string.ascii_uppercase, k=3))
            #                             coupon_code = random_alphabet + "-" + sale.name
            #                             code = api_call.create_coupon(coupon_code, line.price_unit, move_line.quantity)
            #                             picking.coupon_code = code
            #                             created_successfully = True
            #                         else:
            #                             quantities_scanned = True
            #                     else:
            #                         unit_price_not_found = True
            #                 else:
            #                     product_not_found = True

            #             else:
            #                 sale_not_found = True 
            #     else:
            #         picking_not_found = True 
            
            else:
                batch_not_found = True
                
           

        if created_successfully:
            myreturn = [{'status':"Coupon created Successfully and Kindly Validate Batch",
                        'coupon_code':picking.coupon_code}]
        elif quantities_scanned:
            myreturn [{'status':"Can't create coupon all quantities are scanned!"}]

        elif unit_price_not_found:
            myreturn =[{'status':"Quantity or Unit Price not found!"}]

        
        elif product_not_found:
            myreturn = [{'status':"Product not found"}]
        
        elif sale_not_found:
            myreturn = [{'status':"Sale Order not found"}]
        
        elif picking_not_found:
            myreturn = [{'status':"Picking not found"}]
        
        elif batch_not_found:
            myreturn = [{'status':"Batch not found"}]
        
        else:
             myreturn = [{'status':"Error in generating coupon code"}]
        
        return myreturn



# # Single Backorder
# # -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request
# from .. import api_call
# import logging
# import json
# import random
# import string
# from odoo.exceptions import UserError


# _logger_ = logging.getLogger(__name__) 


# class Generate_coupon(http.Controller):


#     @http.route('/generate_coupon',methods=["POST"],type="json",auth="public")
#     def get_coupon(self,**kwargs):
#         move_line_id = kwargs.get('line_id')
#         qty_done = kwargs.get('qty_done')
#         quantity = kwargs.get('quantity')
#         move_id = kwargs.get('move_id')
#         # raise UserError(f'qty_done: {qty_done}, quantity: {quantity}')
#         if not move_line_id:
#             return {
#                 'status':False,
#                 'message':"Stock Line Not Found",
#                 "req":str(kwargs)
#             }
#         move_line=request.env['stock.move.line'].browse(int(move_line_id))
#         if move_line and move_line.batch_id:
#             batch_picking = request.env['stock.picking.batch'].browse(move_line.batch_id.id)
#             if batch_picking and batch_picking.picking_ids:
#                 for picking_id in batch_picking.picking_ids:
#                     picking = request.env['stock.picking'].browse(picking_id.id)
#                     if picking:
#                         if picking.coupon_code:
#                             return {
#                                 'status':"Coupon Code is generated Already!",
#                                 'coupon_code':picking.coupon_code,
#                             }
#                         else:
#                             sale = request.env['sale.order'].browse(picking.sale_id.id)
#                             if sale:
#                                 for line in sale.order_line:
#                                     if line.product_id.id == move_line.product_id.id:
#                                         if move_line.quantity and line.price_unit:
#                                             if line.product_uom_qty > qty_done:
#                                                 random_alphabet = ''.join(random.choices(string.ascii_uppercase, k=3))
#                                                 coupon_code = random_alphabet + "-" + sale.name
#                                                 code = api_call.create_coupon(coupon_code, line.price_unit, move_line.quantity)
#                                                 picking.coupon_code = code
#                                                 picking.create_back_order(qty_done, quantity, move_id)
#                                                 return {
#                                                     'status':"Coupon created Successfully and Batch Validated as well",
#                                                     'coupon_code':picking.coupon_code,
#                                                 }
#                                             else:
#                                                 return {'status':"Can't create coupon all quantities are scanned!"}

#         elif move_line and move_line.picking_id:
#             picking = request.env['stock.picking'].browse(move_line.picking_id.id)
#             if picking:
#                 if picking.coupon_code:
#                     return {
#                         'status':"Coupon Code is generated Already!",
#                         'coupon_code':picking.coupon_code,
#                     }
#                 else:
#                     sale = request.env['sale.order'].browse(picking.sale_id.id)
#                     if sale:
#                         for line in sale.order_line:
#                             if line.product_id.id == move_line.product_id.id:
#                                 if move_line.quantity and line.price_unit:
#                                     if line.product_uom_qty > qty_done:
#                                         code = api_call.create_coupon(picking.coupon_code, line.price_unit, move_line.quantity)
#                                         picking.coupon_code = code
#                                         picking.create_back_order(qty_done, quantity, move_id)
#                                         return {
#                                             'status':"Coupon created Successfully and Batch Validated as well",
#                                             'coupon_code':picking.coupon_code,
#                                         }
#                                     else:
#                                         return {'status':"Can't create coupon all quantities are scanned!"}

#         else:
#             return {
#                 'status':"Batch or picking not found"
#             }    
#         return {
#             'status':"Error in generating coupon code or coupon code generated already",
#         }
