from odoo import models, api, fields

class QuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    is_cluster = fields.Boolean("Include in Cluster", store=True)
    
    cluster_color = fields.Selection([('red', 'Red'), ('blue', 'Blue'), 
                              ('green', 'Green'), ('yellow', 'Yellow')], 
                             string="Cluster Color", store=True)
    clust_color = fields.Char('Cluster Color')
    
                             
    
    @api.model
    def _get_fields_stock_barcode(self):
        fields = super()._get_fields_stock_barcode()
        if 'is_cluster' and 'clust_color' not in fields:
            fields.append('is_cluster')
            fields.append('clust_color')
        return fields


