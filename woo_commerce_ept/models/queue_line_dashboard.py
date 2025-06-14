# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models


class WooQueueLineDashboard(models.AbstractModel):
    _inherit = "queue.line.dashboard"

    def _prepare_query(self, duration, state, table):
        """
        Override the common connector method here to filter out the proper data in order data queue line base on
        order data queue.
        @author: Meera Sidapara @Emipro Technologies Pvt. Ltd on date 10 December 2021 .
        Task_id: 179269 - queue line dashboard
        """
        if table == 'woo_order_data_queue_line_ept':
            queue_type = 'unshipped' if self._context.get('unshipped') else 'shipped'
            qry = """ SELECT oql.id 
                        FROM woo_order_data_queue_line_ept as oql
                        INNER JOIN woo_order_data_queue_ept as oq ON oq.id = oql.order_data_queue_id 
                        AND oq.queue_type = %s 
                        AND oql.state = %s"""
            if duration == 'today':
                qry += " AND oql.create_date >= CURRENT_DATE"
            elif duration == 'yesterday':
                qry += " AND oql.create_date BETWEEN CURRENT_DATE - INTERVAL '1' DAY AND CURRENT_DATE"
            self._cr.execute(qry, (queue_type, state))
            line_ids = self._cr.dictfetchall()
            return [line_id.get('id') for line_id in line_ids]
        else:
            res = super(WooQueueLineDashboard, self)._prepare_query(duration, state, table)
            return res
