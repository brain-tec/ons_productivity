# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#  MIG[10.0] by lfr@open-net.ch (2017)
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from odoo import api, fields, models
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ---------- Fields management

    @api.multi
    @api.depends('subscr_lines.price_subtotal')
    def _subscr_amount_all(self):
        """
        Compute the total amounts of the subscription lines.
        """
        for order in self:
            subscr_amount = 0.0
            for line in order.order_line:
                subscr_amount += line.price_subtotal
            order.update({
                'subscr_amount': subscr_amount
            })

    @api.multi
    @api.depends('order_line.price_total')
    def _quote_amount_all(self):
        """
        Compute the total amounts of the quotation lines.
        """
        for order in self:
            quote_amount_untaxed = quote_amount_tax = 0.0
            for line in order.order_line:
                quote_amount_untaxed += line.price_subtotal
                quote_amount_tax += line.price_tax
            order.update({
                'quote_amount_untaxed': order.pricelist_id.currency_id.round(quote_amount_untaxed),
                'quote_amount_tax': order.pricelist_id.currency_id.round(quote_amount_tax),
                'quote_amount_total': quote_amount_untaxed + quote_amount_tax,
            })

    @api.multi
    @api.depends('order_line.subscr_line_id')
    def _compute_subscription_lines(self):
        for order in self:
            order.subscr_lines = [l.subscr_line_id.id for l in order.order_line if l.subscr_line_id]

    # Hack: avoid sale_contract module's reactions with this field
    subscription_id = fields.Many2one('sale.subscription', 'Subscription', compute=False)

    quot_lines = fields.One2many('sale.order.line', 'order_id', string='Quotations', domain=[('state','in',['draft','sent','cancel'])])
    subscr_lines = fields.One2many('sale.subscription.line', compute='_compute_subscription_lines', string='Subscription lines')

    quote_amount_untaxed = fields.Monetary(string='Untaxed Amount', readonly=True, compute='_quote_amount_all')
    quote_amount_tax = fields.Monetary(string='Taxes', readonly=True, compute='_quote_amount_all')
    quote_amount_total = fields.Monetary(string='Total', readonly=True, compute='_quote_amount_all')

    subscr_amount = fields.Monetary(string='Total', readonly=True, compute='_subscr_amount_all')

    # ---------- UI management

    @api.multi
    def action_confirm(self):

        # Hack: avoid sale_contract module's reactions with this field
        backup = {}
        for order in self:
            backup[order.id] = order.subscription_id
            order.subscription_id = False

        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if backup.get(order.id, False):
                order.subscription_id = backup[order.id]

        return res

    # ---------- Utils

    @api.multi
    def _prepare_invoice(self):
        values = super(SaleOrder, self)._prepare_invoice()
        values['date_invoice'] = datetime.now().strftime(DF)

        return values

    @api.multi
    def write(self, values):
        _logger.info(values)
        if values.get('quot_lines'):
            if values.get('order_line'):
                del values['order_line']
        res = super(SaleOrder, self).write(values)
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')
    subscr_line_id = fields.Many2one('sale.subscription.line', 'Subscription line')

    # ---------- Utils

    @api.multi
    def _prepare_invoice_line(self, qty):
        invoice_line_vals = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if not invoice_line_vals:
            return invoice_line_vals

        for line in self:
            values = {
                'subscription_id': line.subscription_id.id or False,
                'subscr_line_id': line.subscr_line_id.id or False,
                'asset_mrr': 0,
                'asset_start_date': False,
                'asset_end_date': False
            }

            # Overwrite sale_contract_asset's default asset handling:
            #   the info is now computed from the line's recurrence
            #   it defaults from the product if empty
            
            asset_cat = False
            if line.subscr_line_id:
                month = 0
                if line.subscr_line_id.recurring_rule_type in ('dayly','weekly'):
                    month = 0   # i.e. not actually supported
                elif line.subscr_line_id.recurring_rule_type == 'monthly':
                    month = line.subscr_line_id.recurring_interval
                elif line.subscr_line_id.recurring_rule_type == 'yearly':
                    month = 12
                if month:
                    asset_cat = line.env['account.asset.category'].search([('type','=','sale'),('active','=',True),('method_number','=',month)])
                if line.product_id.product_tmpl_id.deferred_revenue_category_id:
                    asset_cat = line.product_id.product_tmpl_id.deferred_revenue_category_id
                if line.subscription_id.asset_category_id:
                    asset_cat = line.subscription_id.asset_category_id

            values['asset_category_id'] = asset_cat and asset_cat.id or False
            if asset_cat and asset_cat.account_asset_id:
                values['account_id'] = asset_cat.account_asset_id.id
            invoice_line_vals.update(values)
        return invoice_line_vals

    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        super(SaleOrderLine, self).invoice_line_create(invoice_id, qty)