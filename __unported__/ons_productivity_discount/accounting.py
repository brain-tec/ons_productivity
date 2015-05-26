# -*- coding: utf-8 -*-
#
#  File: accounting.py
#  Module: ons_productivity_discount
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

import time
import tools
from datetime import datetime
from dateutil.relativedelta import relativedelta
from osv import fields, osv, orm
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class account_payment_term_line(osv.osv):
    _inherit = 'account.payment.term.line'
    
    _columns = {
        'cash_discount_rate': fields.float('Rate', digits_compute=dp.get_precision('Payment Term'), help="Enter a ratio between 0-1."),
        'cash_discount_days': fields.integer('Days', help="Enter the number of days during which the cash discount is valid."),
    }

account_payment_term_line()

class account_payment_term(osv.osv):
    _inherit = 'account.payment.term'

    def compute(self, cr, uid, id, value, date_ref=False, context=None):
        if not date_ref:
            date_ref = datetime.now().strftime('%Y-%m-%d')
        pt = self.browse(cr, uid, id, context=context)
        amount = value
        result = []
        obj_precision = self.pool.get('decimal.precision')
        prec = obj_precision.precision_get(cr, uid, 'Account')
        for line in pt.line_ids:
            if line.value == 'fixed':
                amt = round(line.value_amount, prec)
            elif line.value == 'procent':
                amt = round(value * line.value_amount, prec)
            elif line.value == 'balance':
                amt = round(amount, prec)
            if amt:
                # Amount's date computation
                next_date = (datetime.strptime(date_ref, '%Y-%m-%d') + relativedelta(days=line.days))
                if line.days2 < 0:
                    next_first_date = next_date + relativedelta(day=1,months=1) #Getting 1st of next month
                    next_date = next_first_date + relativedelta(days=line.days2)
                if line.days2 > 0:
                    next_date += relativedelta(day=line.days2, months=1)
                
                # Cash discount's date computation
                next_cash_date = line.cash_discount_rate and (datetime.strptime(date_ref, '%Y-%m-%d') + relativedelta(days=line.cash_discount_days)) or False                

                result.append( (next_date.strftime('%Y-%m-%d'), amt, line.cash_discount_rate, next_cash_date and next_cash_date.strftime('%Y-%m-%d') or False ) )
                amount -= amt

        amount = reduce(lambda x,y: x+y[1], result, 0.0)
        dist = round(value-amount, prec)
        if dist:
            result.append( (time.strftime('%Y-%m-%d'), dist, 0.0, False) )
        return result

account_payment_term()

class account_tax(osv.osv):
    _inherit = 'account.tax'
    
    _columns = {
        'cash_discount_account1_id': fields.many2one('account.account', 'Diff.'),
        'cash_discount_account2_id': fields.many2one('account.account', 'Amount'),
        'cash_discount_woff_tx_acc_id': fields.many2one('account.tax.code', 'Write-off tax account'),
    }

account_tax()

class account_move_line(osv.osv):
    _inherit = 'account.move.line'
    
    _columns = {
        'cash_discount_rate': fields.float('Rate', digits_compute=dp.get_precision('Payment Term'), help="Enter a ratio between 0-1."),
        'cash_discount_date': fields.date('Validity', help="End of cash discount validity"),
    }

account_move_line()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    _columns = {
        'cash_discount_rate': fields.float('Rate', digits_compute=dp.get_precision('Payment Term'), help="Enter a ratio between 0-1."),
        'cash_discount_date': fields.date('Validity', help="End of cash discount validity"),
    }

    def on_change_payment_term(self, cr, uid, ids, date_invoice=False, payment_term=False):
        ret = { 
            'cash_discount_rate': 0.0,
            'cash_discount_date': False,
        }
        today = time.strftime('%Y-%m-%d')
        if payment_term:
            lst = self.pool.get('account.payment.term').compute(cr, uid, payment_term, 1.0, date_ref=date_invoice)
            for item in lst:
                if abs(item[2]) < 0.001 or not item[3]:
                    continue
#                 if today > item[3]:
#                     break
                if ret['cash_discount_rate'] < item[2]:
                    ret = { 
                        'cash_discount_rate': item[2],
                        'cash_discount_date': item[3],
                    }
        
        return { 'value': ret }

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
            
        ret = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,\
                    date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id)
        
        if ret.get('value', {}):
            ret.update(self.on_change_payment_term(cr, uid, ids, date_invoice=date_invoice, payment_term=payment_term)['value'])
        
        return ret

    def finalize_invoice_move_lines(self, cr, uid, invoice_browse, move_lines):
        """Updates the cash discount informations, 
            both in the invoice and the move.line that will be reconciled"""

        move_lines = super(account_invoice, self).finalize_invoice_move_lines(cr, uid, invoice_browse, move_lines)
        if invoice_browse.type not in ['out_invoice','in_invoice'] or not invoice_browse.payment_term: return move_lines

        fld = invoice_browse.type == 'out_invoice' and 'debit' or 'credit'
        today = time.strftime('%Y-%m-%d')
        cash_discount = self.on_change_payment_term(cr, uid, [], date_invoice=invoice_browse.date_invoice or today, payment_term=invoice_browse.payment_term.id)
        invoice_browse.write(cash_discount['value'])
        for line_id in range(len(move_lines)):
            vals = {
                'cash_discount_rate': 0.0,
                'cash_discount_date': False,
            }
            if move_lines[line_id][2].get(fld, False):
                vals.update({
                    'cash_discount_rate': invoice_browse.cash_discount_rate,
                    'cash_discount_date': invoice_browse.cash_discount_date,
                })
            move_lines[line_id][2].update(vals)
        
        return move_lines
        
account_invoice()

class account_move(osv.osv):
    _inherit = 'account.move'

    def create(self, cr, uid, vals, context={}):
        return super(account_move, self).create(cr, uid, vals, context=context)

account_move()

class payment_line(osv.osv):
    _inherit = 'payment.line'

    _columns = {
        'cash_discount_rate': fields.float('Rate', digits_compute=dp.get_precision('Payment Term'), readonly=True),
        'cash_discount_date': fields.date('Validity', readonly=True),
        'cash_discount_applied': fields.boolean('Applied', readonly=True),
        'cash_discount_org': fields.float('Org. amount', readonly=True),
    }

payment_line()
