from odoo import api, fields, models
from odoo.exceptions import UserError

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"
    is_put = fields.Boolean('Put in a Pack')
   