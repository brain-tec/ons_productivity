# -*- coding: utf-8 -*-
#
#  File: partners.py
#  Module: ons_productivity_credit_control
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
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

from osv import fields, osv, orm

import logging
_logger = logging.getLogger(__name__)

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
        'ons_invoice_ids': fields.one2many('account.invoice', 'partner_id', 'Invoices', domain=[('type','in',['out_invoice','in_invoice'])]),
        'ons_refund_ids': fields.one2many('account.invoice', 'partner_id', 'Refunds', domain=[('type','in',['out_refund','in_refund'])]),
    }

res_partner()
