# -*- encoding: utf-8 -*-
#
#  File: models/partners.py
#  Module: ons_productivity_product_variants
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ---------- Fields management

    ons_supplier_currency = fields.Many2one('res.currency',
        string='Price List Currency')

