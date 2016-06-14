# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_productivity_sol_req
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
##############################################################################
#    
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################


from openerp import models, fields, api
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # ---------- Fields management

    requested_date = fields.Date(string='Requested Date',
        readonly=True, 
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]}, 
        copy=False
    )

    # ---------- Tools

    def _prepare_order_line_procurement(self, cr, uid, ids, group_id=False, context=None):
        vals = super(SaleOrderLine, self)._prepare_order_line_procurement(cr, uid, ids, group_id=group_id, context=context)
        line = self.browse(cr, uid, ids, context=context)
        if line.requested_date:
            date_planned = datetime.strptime(line.requested_date + ' 00:00:00', DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(days=line.order_id.company_id.security_lead)
            vals.update({
                'date_planned': date_planned.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            })
        return vals


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ---------- Fields management

    @api.one
    @api.depends('requested_date', 'order_line.requested_date')
    def _check_requested_dates(self):
        self.hide_requested_date = False
        ref_date = False
        for line in self.order_line:
            if not line.requested_date:
                continue
            if not ref_date:
                ref_date = line.requested_date
                continue
            if ref_date != line.requested_date:
                self.hide_requested_date = True
                break

    hide_requested_date = fields.Boolean(compute='_check_requested_dates', 
                                         string='Must hide requested date',
                                         default=False
    )

