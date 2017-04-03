# -*- coding: utf-8 -*-
#
#  File: models/invoices.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#  MIG[10.0] by lfr@open-net.ch (2017)
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')
    subscr_line_id = fields.Many2one('sale.subscription.line', 'Subscription line')
    asset_start_date = fields.Date(string='Asset End Date', compute='_get_asset_date', readonly=True, store=True)
    asset_end_date = fields.Date(string='Asset Start Date', compute='_get_asset_date', readonly=True, store=True)

    @api.multi
    @api.depends('asset_category_id', 'invoice_id.date_invoice', 'price_subtotal_signed')
    def _get_asset_date(self):
        for invoice in self:
            invoice.asset_mrr = 0
            invoice.asset_start_date = False
            invoice.asset_end_date = False
            cat = invoice.asset_category_id
            if cat:
                months = cat.method_number * cat.method_period
                if invoice.invoice_id.type in ['out_invoice', 'out_refund']:
                    invoice.asset_mrr = invoice.price_subtotal_signed / months
                if invoice.invoice_id.date_invoice:
                    start_date = datetime.strptime(invoice.invoice_id.date_invoice, DF)
                    end_date = (start_date + relativedelta(months=months, days=-1))
                    invoice.asset_start_date = start_date.strftime(DF)
                    invoice.asset_end_date = end_date.strftime(DF)

    # ---------- Instances management

    @api.model
    def create(self, vals):
        return super(AccountInvoiceLine, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(AccountInvoiceLine, self).write(vals)

