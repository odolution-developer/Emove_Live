from odoo import api, fields, models
from odoo.exceptions import UserError
from .. import api_call
import random
import string
from odoo.tools.float_utils import float_is_zero, float_compare

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _get_fields_stock_barcode(self):
        fields = super()._get_fields_stock_barcode()
        # Add 'standard_price' if it's not already in the list
        if 'state' not in fields:
            fields.append('state')
        return fields
    
    # Single Back Order
    # def create_back_order(self, qty_done, quantity, move_id):
    #     line_to_proceed = []
    #     for line in self.move_ids:
    #         if move_id == line.id:
    #             line_to_proceed.append(line)
                


    #     if line_to_proceed and self.state not in ['done, draft, cancel']:
    #         for line in line_to_proceed:        
    #             if qty_done < line.product_uom_qty:
    #                 line.quantity = line.product_uom_qty - qty_done
    #                 line.product_uom_qty = line.product_uom_qty - qty_done
    #         # raise UserError(str(line_to_proceed))
    #         backorder = self.env['stock.picking'].create({
    #         'backorder_id': self.id,
    #         'partner_id': self.partner_id.id,
    #         'location_id': self.location_id.id,
    #         'location_dest_id': self.location_dest_id.id,
    #         'scheduled_date': self.scheduled_date,
    #         'date_deadline': self.scheduled_date,
    #         'origin': self.origin,
    #         'user_id': self.user_id.id,
    #         'company_id': self.env.company.id,
    #         'picking_type_id': self.picking_type_id.id,
    #         'move_type': self.move_type,
    #         'move_ids': [(6, 0, [line.id for line in line_to_proceed])],
    #         'move_line_ids_without_package':[(6, 0, [line.id for move in line_to_proceed for line in move.move_line_ids])],

    #         'state': 'confirmed',
    #         })
    #         for line in self.move_ids:
    #             if qty_done < line.product_uom_qty:
    #                 line.quantity = qty_done
    #                 line.product_uom_qty = qty_done
    #         self.state = "done"
    #         if self.batch_id:
    #             batch_transfer = self.env['stock.picking.batch'].search([('id', '=', self.batch_id.id)])
    #             if batch_transfer:
    #                 batch_transfer.state = "done" 

    # Multiple Backorder 
    def create_back_order(self, qty_done, quantity, move_id, picking_id):
        try: 
                
            current_picking = self.env['stock.picking'].search([('id', '=', picking_id)])
            line_to_proceed = []
            for line in current_picking.move_ids:
                if move_id == line.id:
                    line_to_proceed.append(line)
                    
            for line in current_picking.move_ids:
                if move_id == line.id:
                    line.product_uom_qty = line.product_uom_qty - qty_done
                    line.quantity = line.product_uom_qty - qty_done


            if line_to_proceed and current_picking.state not in ['done, draft, cancel']:
                for line in line_to_proceed:        
                    if qty_done < quantity:
                        line.product_uom_qty = qty_done
                        line.quantity = qty_done
                # raise UserError(str(line_to_proceed))
                try:
                    backorder = self.env['stock.picking'].create({
                    'backorder_id': current_picking.id,
                    'partner_id': current_picking.partner_id.id,
                    'location_id': current_picking.location_id.id,
                    'location_dest_id': current_picking.location_dest_id.id,
                    'scheduled_date': current_picking.scheduled_date,
                    'date_deadline': current_picking.scheduled_date,
                    'origin': current_picking.origin,
                    'user_id': current_picking.user_id.id,
                    'company_id': current_picking.env.company.id,
                    'picking_type_id': current_picking.picking_type_id.id,
                    'move_type': current_picking.move_type,
                    'move_ids': [(6, 0, [line.id for line in line_to_proceed])],
                    # 'move_line_ids_without_package':[(6, 0, [line.id for move in line_to_proceed for line in move.move_line_ids])],

                    'state': 'confirmed',
                    })
                except Exception as e:
                    print("Unexpeted Error")
                current_picking.state = "done"
                if current_picking.batch_id:
                    batch_transfer = self.env['stock.picking.batch'].search([('id', '=', current_picking.batch_id.id)])
                    if batch_transfer:
                        return batch_transfer
        except Exception as e:
            print("Unexpected Error")
        return None
                # raise UserError('Working' + "qty_done: " + str(qty_done) + "quantity: " + str(quantity) + "move Line id: " + str(move_id))
            # raise UserError(str(backorder.move_line_ids_without_package))
            
    stage_id = fields.Many2one('picking.stages', string="Stages")    
    state_helper = fields.Boolean(string='State Compute Helper', compute="_compute_state_helper") #, compute="_compute_state_helper"
    # woo_order_status = fields.Char(string = 'Woo Order Status', compute="_compute_woo_order_status")
    currency_id = fields.Many2one('res.currency', string="Currency",
        related='company_id.currency_id',
        default=lambda
        self: self.env.user.company_id.currency_id.id)
    
    amount_total = fields.Monetary(string = "Amount Total", related= "sale_id.amount_total")
    is_batch = fields.Boolean(string= "Include in Batch")
    coupon_code = fields.Char(string = "Coupon Code", store=True, readonly=True)
    is_coupon_generate = fields.Boolean(string = "Is Coupon Generate")
            
    @api.depends('state', 'batch_id')
    def _compute_state_helper(self):
        for picking in self:
            picking.stage_id = False
            picking.state_helper = False
            stage_type = False
            if picking.sale_id and picking.move_ids:
                pick = self.env["stock.picking"].search([('sale_id', '=', picking.sale_id.id), ('picking_type_id.sequence_code', '=', 'PICK'), ('backorder_id', '=', False)], limit=1)
                back_pick = self.env["stock.picking"].search([('sale_id', '=', picking.sale_id.id), ('picking_type_id.sequence_code', '=', 'PICK'), ('backorder_id', '=', pick.id)], limit=1)
                if all(move.quantity == move.product_uom_qty for move in picking.move_ids) and picking.state in ['done'] or (back_pick and back_pick.state in ['done']):
                    stage_type = 'complete'

                elif picking.state in ['done'] and (any(move.quantity != move.product_uom_qty for move in picking.move_ids) or picking.backorder_id) and back_pick and back_pick.state not in ['done']:
                    stage_type = 'incomplete_orders'
                elif picking.state not in ['draft', 'done', 'cancel'] and picking.sale_id:
                    if picking.picking_type_id.sequence_code == "PICK":
                        if picking.batch_id:
                            stage_type = 'perparation_phase'
                        elif not picking.batch_id:
                            stage_type = 'processing'
                    elif picking.picking_type_id.sequence_code == "OUT":
                        if pick and pick.state == 'done' and picking.batch_id:
                            stage_type = 'ready_to_send'
                        elif not picking.batch_id:
                            stage_type = 'processing'
                        elif picking.batch_id:
                            stage_type = 'perparation_phase'

            # Assign stage
            if stage_type:
                stage = self.env['picking.stages'].search([('type', '=', stage_type)], limit=1)
                picking.stage_id = stage.id
            

            picking.state_helper = True
    
    # def _compute_woo_order_status(self):
    #     for picking in self:
    #         order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
    #         # raise UserError(str(order.id))
    #         if order and order.woo_order_id:
    #             status = api_call.fetch_order_status(order.woo_order_id)
    #             picking.woo_order_status = status
    #             picking.stage_id.woo_type = status
                            
    def action_open_add_to_stage_wizard(self):

        pickings = self.env['stock.picking'].search([('is_batch', '=', True)])
        if pickings:
            return {
                'name': 'Add to Batch',
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking.to.batch',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'active_id': self.id,
                    'default_user_id': self.env.uid,
                },
            }
        else:  
            batch = self.env['stock.picking.batch'].create({
            'user_id': self.env.uid,
            'company_id': self.env.company.id,
            'picking_type_id': self.picking_type_id.id,
            'picking_id':self.id,
            'state': 'in_progress',
            })
            self.batch_id = batch.id

    # def create(self,vals):
    #     res = super().create(vals)
    #     for rec in res:
    #         rec._compute_woo_order_status()
    #     return res

    # def write(self, vals):
    #     pick_stage1 = self.stage_id.name
    #     res = super().write(vals)
    #     pick_stage2 = False

    #     for picking in self:
    #         if pick_stage1 != pick_stage2:
    #             # Define pick and back_pick early
    #             pick = self.env["stock.picking"].search([
    #                 ('sale_id', '=', picking.sale_id.id),
    #                 ('picking_type_id.sequence_code', '=', 'PICK'),
    #                 ('backorder_id', '=', False)
    #             ], limit=1)

    #             back_pick = self.env["stock.picking"].search([
    #                 ('sale_id', '=', picking.sale_id.id),
    #                 ('picking_type_id.sequence_code', '=', 'PICK'),
    #                 ('backorder_id', '=', pick.id)
    #             ], limit=1)

    #             order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)

    #             if 'batch_id' in vals.keys():
    #                 # raise UserError('Hit 1')
    #                 if pick.batch_id and order:
    #                     api_call.update_order_status(order.woo_order_id, "220perparation_")
    #             else:
    #                 # raise UserError('Hit 2')
    #                 if picking.batch_id and picking.move_ids:
    #                     if picking.state == 'done' and (all(move.quantity != move.product_uom_qty for move in picking.move_ids) or picking.backorder_id):
    #                         api_call.update_order_status(order.woo_order_id, "776incompleteor")
    #                     elif all(move.quantity == move.product_uom_qty for move in picking.move_ids) and picking.state == 'done':
    #                         api_call.update_order_status(order.woo_order_id, "complete")
    #                     elif picking.picking_type_id.sequence_code == "OUT" and pick and pick.state == 'done':
    #                         api_call.update_order_status(order.woo_order_id, "ready_to_send")
    #     return res

