from odoo import api, fields, models
from odoo.exceptions import UserError


class PickingStages(models.Model):
    _name = "picking.stages"
    

    name= fields.Char("Name")
    type = fields.Selection([('processing', 'Processing'), ('perparation_phase', 'Perparation Phase'), 
                              ('ready_to_send', 'Ready To Send'), ('incomplete_orders', 'Incomplete Orders'), 
                              ('complete', 'Completed')], 
                             string="Type", store=True)
    woo_type = fields.Selection([('processing', 'Processing'), ('220perparation_', 'Perparation Phase'), 
                              ('ready_to_send', 'Ready To Send'), ('776incompleteor', 'Incomplete Orders'), 
                              ('complete', 'Completed')], 
                             string="Woo Status Type", store=True)
    
