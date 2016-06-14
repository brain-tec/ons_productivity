# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ---------- Fields management

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

    @api.one
    @api.depends('order_line.subscr_line_id')
    def _compute_subscription_lines(self):
        self.subscr_lines = [l.subscr_line_id.id for l in self.order_line if l.subscr_line_id]

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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')
    subscr_line_id = fields.Many2one('sale.subscription.line', 'Subscription line')

