# -*- coding: utf-8 -*-
#
#  File: models/products.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#  MIG[10.0] by lfr@open-net.ch (2017)
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ---------- Fields management

    recurring_rule_type = fields.Selection([
            ('none', 'None'),
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)')],
            'Recurrency',
            required=True,
            help="Invoice automatically repeat at specified interval",
            default=lambda *a: 'none')

    recurring_interval = fields.Integer(
            'Interval',
            help="Repeat every (Days/Week/Month/Year)",
            default=lambda *a: 1)
