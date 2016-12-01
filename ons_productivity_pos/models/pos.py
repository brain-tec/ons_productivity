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

class PosSession(models.Model):
    _inherit = 'pos.session'    

    def _check_unicity(self, cr, uid, ids, context=None):
        return True
    _constraints = [
        (_check_unicity, "You cannot create two active sessions with the same responsible!", ['user_id', 'state'])
    ]
