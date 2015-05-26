# -*- coding: utf-8 -*-
#
#  File: account_payments.py
#  Module: ons_cust_edsi_tech
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

from osv import fields, osv
from openerp.tools.translate import _
import os
import base64

import tools
import re
import unicodedata

import time

import logging
_logger = logging.getLogger(__name__)

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', tools.ustr(value)).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())

    return re.sub('[-\s]+', '-', value)

class account_payment(osv.osv):
    _inherit = 'payment.order'
    
    # ------------------------- Scheduler management
    
    def handle_payment_dtas(self, cr, uid, context={}):
        _logger.info("Starting the management of account payment dta files")
        
        payment_orders = self.pool.get('payment.order')
        params = self.pool.get('ons.account_statement.params').get_instance(cr, uid, context=context)
        if not params or not params.directory_out or not os.path.isdir(params.directory_out):
            _logger.info(" => config problem: invalid output directory")
            return False
        
        for po_id in payment_orders.search(cr, uid, [('state', '=', 'open')], context=context):
            po_name = payment_orders.read(cr, uid, po_id, ['reference'], context=context)['reference']
            _logger.info(" => Handling '%s'" % po_name)
            
            ctx = {
                'active_ids': [po_id],
                'active_id': po_id,
            }
            dta_content = self.pool.get('create.dta.wizard').create_dta(cr, uid, [], context=ctx)
            if not dta_content:
                _logger.info("Payment '%s': nothing to save" % po_name)
                continue
            #f_name = os.path.normpath(params.directory_out) + "/%s.dta" % slugify(po_name)
            f_name = os.path.normpath(params.directory_out) + time.strftime("/DTAN_8292768_%Y%m%d_%H%I%S.TXT")
            f = False
            try:
                f = open(f_name, 'w')
            except:
                pass
            if not f:
                _logger.info(" => Can't create/open '%s'" % f_name)
                continue
            f.write(base64.decodestring(dta_content))
            f.close()

        _logger.info("End the management of account payment dta files")

account_payment()
