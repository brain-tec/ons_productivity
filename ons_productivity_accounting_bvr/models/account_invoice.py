# -*- coding: utf-8 -*-
#
#  File: accounts.py
#  Module: ons_productivity_accounting_bvr
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015 Open-Net Ltd. All rights reserved.
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp import models, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id_set_bank(self):
        super(AccountInvoice, self).onchange_partner_id_set_bank()
        if self.type not in ('in_invoice', 'in_refund'):
            user = self.env.user
            bank_ids = user.company_id.partner_id.bank_ids
            for bank in bank_ids:
                if bank.type == 'bvr':
                    self.partner_bank_id = bank
                    break
