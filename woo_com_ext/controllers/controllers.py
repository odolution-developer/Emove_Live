
from odoo import http
from odoo.http import request, Response
import json

class PurchaseOrderAPI(http.Controller):

    @http.route('/api/expected_purchase_date', auth='public', methods=['GET'], cors='*', csrf=False)
    def get_specific_product(self, **kw):
        try:
            id = kw['id']
            woo_id=request.env['woo.product.product.ept'].sudo().search([('variant_id', '=', id)],limit=1).product_id.id


            po_lines = request.env['purchase.order.line'].sudo().search([
                ('product_id', '=', woo_id),
                ('order_id.state', 'in', ['purchase', 'done'])  # Ensure only confirmed/done orders
            ],  order='id desc', limit=1)

            if po_lines:
                expected_date = po_lines.order_id.date_planned
                product_list = {
                    'id':po_lines.name,
                    'name':po_lines.order_id.name,
                    'expected_date': expected_date.strftime('%d-%m-%Y'),

                }
                data = json.dumps(product_list)
                return data
            else:
                data = json.dumps({'status': False, 'code': 'No product found'})
                return data
        except Exception as e:
            return str(e)

