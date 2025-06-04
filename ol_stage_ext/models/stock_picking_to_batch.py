from odoo import models, api, _
from odoo.exceptions import UserError


class StockPickingToBatch(models.TransientModel):
    _inherit = 'stock.picking.to.batch'

    def attach_pickings(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search(['|',
            ('id', 'in', self.env.context.get('active_ids', [])),
             ('is_batch', '=', True)])
        if self.mode == 'new':
            company = pickings.company_id
            if len(company) > 1:
                raise UserError(_("The selected pickings should belong to an unique company."))
            batch = self.env['stock.picking.batch'].create({
                'user_id': self.user_id.id,
                'company_id': company.id,
                'picking_type_id': pickings[0].picking_type_id.id,
            })
        else:
            batch = self.batch_id

        pickings.write({'batch_id': batch.id})
        # you have to set some pickings to batch before confirm it.
        if self.mode == 'new' and not self.is_create_draft:
            batch.action_confirm()
        
        for pick in pickings:
            pick.is_batch = False
