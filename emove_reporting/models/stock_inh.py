
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_weight = fields.Float(string="Total Weight", compute="_compute_total_weight", store=True)
    is_weight_below_threshold = fields.Boolean(string="Is Weight Below 10", compute="_compute_is_weight_below_threshold", store=True)

    @api.depends('move_ids_without_package.product_uom_qty', 'move_ids_without_package.product_id.weight')
    def _compute_total_weight(self):
        for picking in self:
            total_weight = sum(move.product_uom_qty * move.product_id.weight for move in picking.move_ids_without_package)
            picking.total_weight = total_weight

    @api.depends('total_weight')
    def _compute_is_weight_below_threshold(self):
        for picking in self:
            picking.is_weight_below_threshold = picking.total_weight < 10


    def get_cluster_lines(self, docs):
        # print(docs.mapped('move_ids_without_package').ids)
        # print(self.env['stock.move'].search([('id', 'in', docs.mapped('move_ids_without_package').ids)],  order='product_id desc'))
        # reached_goals = self.env['stock.move']._read_group([
        #     ('id', 'in', docs.mapped('move_ids_without_package').ids),
        # ], groupby=['product_id'], aggregates=['__count'])
        # print(reached_goals)
        move_lines = self.env['stock.move'].search([('id', 'in', docs.mapped('move_ids_without_package').ids)]).sorted(
            key=lambda r: r.product_id.default_code or '.')
        return move_lines