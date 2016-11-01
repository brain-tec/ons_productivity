# -*- coding: utf-8 -*-
#
#  File: models/products.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################

from openerp.osv import osv, fields


class ProductTemplate(osv.osv):
    _inherit = 'product.template'

    # ---------- Fields management

    _columns = {
        'recurring_rule_type': fields.selection([
                ('none', 'None'),
                ('daily', 'Day(s)'),
                ('weekly', 'Week(s)'),
                ('monthly', 'Month(s)'),
                ('yearly', 'Year(s)'), ],
            'Recurrency',
            required=True,
            help="Invoice automatically repeat at specified interval"),
        'recurring_interval': fields.integer(
            'Interval',
            help="Repeat every (Days/Week/Month/Year)"),
    }
    _defaults = {
        'recurring_rule_type': lambda *a: 'none',
        'recurring_interval': lambda *a: 1,
    }
