# -*- coding: utf-8 -*-
#
#  File: models/pos.py
#  Module: ons_productivity_pos
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


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # ---------- Fields management
    
    pos_default_customer = fields.Many2one('res.partner', string='Default customer')
