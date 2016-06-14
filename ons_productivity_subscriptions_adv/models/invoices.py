# -*- coding: utf-8 -*-
#
#  File: models/invoices.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # ---------- Fields management

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')
    subscr_line_id = fields.Many2one('sale.subscription.line', 'Subscription line')

