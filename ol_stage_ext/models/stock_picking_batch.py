from odoo import api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking.batch"

    stage_id = fields.Many2one('picking.stages', string="Stages")    
    state_helper = fields.Boolean('State Compute Helper', compute="_compute_state_helper")
    picking_id = fields.Many2one('stock.picking', string="Picking")

    currency_id = fields.Many2one('res.currency', string="Currency")
    
    sale_id = fields.Many2one('sale.order', string="Sale")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier")
    scheduled_date = fields.Datetime(string="Scheduled Date")

    
    amount_total = fields.Monetary(string = "Amount Total")
    weight = fields.Float(string = "Weight")
    sequence_help = fields.Boolean('Sequence Help', compute="compute_sequence_help")

    @api.depends('move_ids')
    def compute_sequence_help(self):
        for batch in self:
            all_moves = batch.picking_ids.mapped('move_ids')
            sorted_moves = sorted(all_moves, key=lambda m: m.product_id.default_code or '')
            for i, move in enumerate(sorted_moves, start=1):
                move.sequence = i 
            batch.sequence_help = True
    
    @api.depends('state', 'picking_ids')
    def _compute_state_helper(self):

        for batch in self:
            batch.picking_id = False
            batch.state_helper = False
            for line in batch.picking_ids:
                picking_name = line.name
                if picking_name:
                    picking = self.env['stock.picking'].search([('name', '=', picking_name)], limit=1)
                    if picking:
                        batch.picking_id = picking.id
                        batch.scheduled_date = picking.scheduled_date
                        batch.weight = picking.weight
                        if picking.carrier_id:
                            batch.carrier_id = picking.carrier_id.id
                        if picking.currency_id:
                            batch.currency_id = picking.currency_id.id
                        sale = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                        if sale:
                            batch.sale_id = sale.id
                            batch.amount_total = sale.amount_total                                    


                    stage_type = False
                    # Check each condition individually
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

                    if stage_type:
                        stage = self.env['picking.stages'].search([('type', '=', stage_type)], limit=1)

                        batch.stage_id = stage.id
                    else:
                        batch.stage_id = False
                    
                batch.state_helper = True

    