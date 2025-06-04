from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductVariant(models.Model):
    _inherit = "product.product"

    @api.model
    def _get_fields_stock_barcode(self):
        fields = super()._get_fields_stock_barcode()
        # Add 'standard_price' if it's not already in the list
        if 'standard_price' not in fields:
            fields.append('standard_price')
        if 'package_id' not in fields:
            fields.append('package_id')
        if 'packages' not in fields:
            fields.append('packages')
        return fields

    package_id = fields.Many2one('stock.quant.package', string = 'Packages', compute = 'compute_package_id', store=True)
    packages = fields.Json("Packages", compute = "compute_packages")


    def compute_package_id(self):
        for rec in self:
            packages = self.env['stock.quant.package'].search([('is_cluster', '=', True)])
            for pack in packages:

                if pack.quant_ids:
                    # for line in pack.quant_ids:
                    if any(line.product_id.name == rec.name for line in pack.quant_ids):
                        rec.package_id = pack.id
                        break

    def compute_packages(self):
        for rec in self:
            result = {}
            packages = self.env['stock.quant.package'].search([('is_cluster', '=', True)])  
            for pack in packages:
                result[pack.name] = pack.clust_color
            # raise UserError(str(result))
            rec.packages = result  
