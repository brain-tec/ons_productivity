# -*- coding: utf-8 -*-
#
#  File: models/products.py
#  Module: ons_tools_unbalanced_moves
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################


from openerp import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def assert_balanced(self):
        return True
