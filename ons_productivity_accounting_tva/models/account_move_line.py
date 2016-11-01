# -*- coding: utf-8 -*-
#
#  File: models/account_move_line.py
#  Module: ons_productivity_accounting_tva
#
#  dco@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ons_taxes_tags = fields.Many2many('account.account.tag', string='Taxes tags')

    @api.model
    def get_tags_from_tax(self):
        for line in self.search([]):
                if line.tax_line_id:
                    line.ons_taxes_tags = line.tax_line_id.tag_ids.ids

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def post(self):
        res = super(AccountMove, self).post()
        for move in self:
            for line in move.line_ids:
                if line.tax_line_id:
                    line.ons_taxes_tags = line.tax_line_id.tag_ids.ids
        return res
