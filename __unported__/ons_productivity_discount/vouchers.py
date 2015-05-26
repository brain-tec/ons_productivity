# -*- coding: utf-8 -*-
#
#  File: vouchers.py
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
from osv import fields, osv, orm
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    def action_move_line_create(self, cr, uid, ids, context=None):
        '''
        Confirm the vouchers given in ids and create the journal entries for each of them
        '''
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        inv_pool = self.pool.get('account.invoice')
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.move_id:
                continue
            
            current_currency_obj = voucher.currency_id or voucher.journal_id.company_id.currency_id
            company_currency = self._get_company_currency(cr, uid, voucher.id, context)
            current_currency = self._get_current_currency(cr, uid, voucher.id, context)
            # we select the context to use accordingly if it's a multicurrency case or not
            context = self._sel_context(cr, uid, voucher.id, context)
            # But for the operations made by _convert_amount, we always need to give the date in the context
            ctx = context.copy()
            ctx.update({'date': voucher.date})
            # Create the account move record.
            move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
            # Get the name of the account_move just created
            name = move_pool.browse(cr, uid, move_id, context=context).name

            # Create the first line of the voucher
            ref_move_line = self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, context)
            move_line_id = move_line_pool.create(cr, uid, ref_move_line, context)
            move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
            line_total = move_line_brw.debit - move_line_brw.credit
            rec_list_ids = []
            if voucher.type == 'sale':
                line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            elif voucher.type == 'purchase':
                line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)

            # Create one move line per voucher line where amount is not 0.0
            balance, rec_list_ids = self.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

            # New: the writeoff is not completely dropped into its account, as long as the 1st corresponding invoice linked to the move-id as taxes:
            #   - untaxed amount is dedicated to the actual writeoff
            #   - a new move-line is appended to return the tax on the writeoff back to the first tax financial account found
            tx_move_lines = {}
            tx_tot = 0.0
            writeoff_tx_acc = False  # tax account on write-off
            writeoff_account = False # cash discountaccount on write-off
            wo_move_lines = {}
            grand_total = 0.0
            if not currency_obj.is_zero(cr, uid, current_currency_obj, balance):
                tax = False
                today = time.strftime('%Y-%m-%d')
                bal_sign = balance < 0 and -1.0 or 1.0
                for ln in voucher.line_ids:
                    if not ln.move_line_id: continue
                    grand_total += ln.amount #_unreconciled
                    bal_vl = abs(balance * line_total / ln.amount_original)
                    
                    inv_ids = inv_pool.search(cr, uid, [('move_id','=',ln.move_line_id.move_id.id)], context=context)
                    if not inv_ids: continue
                    
                    for inv in inv_pool.browse(cr, uid, inv_ids, context=context):
                        # any cash rate?
                        if abs(inv.cash_discount_rate) < 0.0001: continue
                        # Still valid?
                        if inv.cash_discount_date < today: continue
                        # Nothing to pay?
                        if abs(inv.amount_untaxed) < 0.001: continue
                        bal_inv = abs(bal_vl * ln.amount_original / inv.amount_untaxed)
                        # Valid taxes and accounts?
                        for invl in inv.invoice_line:
                            if not invl.invoice_line_tax_id: continue
                            if abs(invl.price_subtotal) < 0.001: continue
                            t=invl.price_subtotal
                            bal_invl = abs(bal_inv * invl.price_subtotal / inv.amount_total)

                            if inv.type == 'out_invoice':
                                fld = 'debit'
                                tx_sign = -1.0
                            else:
                                fld = 'credit'
                                tx_sign = 1.0
                            
                            taxes = []
                            for tx in invl.invoice_line_tax_id:
                                if not tx.cash_discount_account1_id or not tx.cash_discount_account2_id: continue
                                taxes += [tx]
                                
                                if tx.cash_discount_woff_tx_acc_id and not writeoff_tx_acc:
                                    writeoff_tx_acc  = tx.cash_discount_woff_tx_acc_id.id
                                    writeoff_account = tx.cash_discount_account2_id.id
                                
                            # res_lst looks like this:
                            #     [
                            #      {'account_analytic_collected_id': False,
                            #       'account_analytic_paid_id': False,
                            #       'account_collected_id': 1460,
                            #       'account_paid_id': 1460,
                            #       'amount': 0.7407407407407408,
                            #       'base_code_id': 34,
                            #       'base_sign': 1.0,
                            #       'id': 16,
                            #       'name': u'TVA due a 8.0% (TN)',
                            #       'price_unit': 9.25925925925926,
                            #       'ref_base_code_id': 34,
                            #       'ref_base_sign': -1.0,
                            #       'ref_tax_code_id': 31,
                            #       'ref_tax_sign': -1.0,
                            #       'sequence': 1,
                            #       'tax_code_id': 31,
                            #       'tax_sign': 1.0,
                            #       'todo': 0},
                            #      {....},
                            #      {....},
                            #      ]
        
                            if not taxes:
                                res_lst = []
                            else:
                                res_lst = self.pool.get('account.tax')._unit_compute_inv(cr, uid, taxes, bal_invl)
                            for res in res_lst:

                                tax_bal = res['amount']
                                tx_tot += tax_bal
                                balance = (abs(balance) - tax_bal) * bal_sign
                                
                                tx = self.pool.get('account.tax').browse(cr, uid, res['id'], context=context)

                                tx_move_line = {
                                    'journal_id': voucher.journal_id.id,
                                    'period_id': voucher.period_id.id,
                                    'name': 'Dim TVA due / ' + tx.name,
                                    'account_id': tx.cash_discount_account1_id.id,
                                    'move_id': move_id,
                                    'partner_id': voucher.partner_id.id,
                                    'currency_id': company_currency <> current_currency and current_currency or False,
                                    'analytic_account_id': voucher.analytic_id and voucher.analytic_id.id or False,
                                    'quantity': 1,
                                    'credit': 0.0,
                                    'debit': 0.0,
                                    'date': voucher.date,
                                }
                                tx_move_line[fld] = tax_bal
                                if tx.tax_code_id:
                                    tx_move_line.update({
                                        'tax_code_id': tx.tax_code_id.id,
                                        'tax_amount': tax_bal * tx_sign
                                    })
                                
                                key = str(tx.id)
                                if key not in tx_move_lines:
                                    tx_move_lines[key] = tx_move_line
                                else:
                                    tx_move_lines[key]['debit'] += tx_move_line['debit']
                                    tx_move_lines[key]['credit'] += tx_move_line['credit']
                                    if tx_sign < 0:
                                        tx_move_lines[key]['tax_amount'] -= tx_move_line['tax_amount']
                                    else:
                                        tx_move_lines[key]['tax_amount'] += tx_move_line['tax_amount']
                                if tx.cash_discount_account2_id and tx.cash_discount_woff_tx_acc_id:
                                    if key not in wo_move_lines:
                                        wo_move_lines[key] = {
                                            'account': tx.cash_discount_account2_id.id,
                                            'tx_acc' : tx.cash_discount_woff_tx_acc_id.id,
                                            'amount' : abs(tax_bal),
                                        }
                                    else:
                                        wo_move_lines[key] += abs(tax_bal)
            
            # Create the writeoff line if needed
            #balance = bal_sign * (grand_total - line_total)
            bal_diff = abs(grand_total - line_total - abs(balance))
            if len(wo_move_lines) > 0:
                wo_tot = reduce(lambda x,y: x+y['amount'], [wo_move_lines[x] for x in wo_move_lines], 0)
                wo_bal = abs(grand_total - line_total - abs(balance))
                for key,wo_move_line in wo_move_lines.items():
                    wo_val = balance * wo_move_line['amount'] / wo_tot
                    wo_bal -= wo_val
                    _logger.debug(" **************************************** WO_BAL is"+str(wo_bal) )
#                     if abs(wo_bal) < 0.05:
#                         wo_val -= wo_bal
                    ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, wo_val, move_id, name, company_currency, current_currency, context)
                    if not ml_writeoff: continue
                    ml_writeoff.update({
                        'account_id': wo_move_line['account'],
                        'tax_code_id': wo_move_line['tx_acc'],
                        'tax_amount': -1.0 * abs(wo_val)
                    })
                    
                    new_id = move_line_pool.create(cr, uid, ml_writeoff, context)
#                     if new_id:
#                         rec_list_ids += [new_id]
            else:
                ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, balance, move_id, name, company_currency, current_currency, context)
                if ml_writeoff:
                    move_line_pool.create(cr, uid, ml_writeoff, context)
            
            for key,tx_move_line in tx_move_lines.items():
                move_line_pool.create(cr, uid, tx_move_line, context)
            
            cr.execute("Select sum(debit) - sum(credit) from account_move_line where move_id=" + str(move_id))
            row = cr.fetchone()
            if row[0] > 0.0:
                cr.execute("Update account_move_line set debit=debit-"+str(row[0])+" where id="+str(move_line_id))
            elif row[0] < 0.0:
                cr.execute("Update account_move_line set credit=credit-"+str(row[0])+" where id="+str(move_line_id))
                
            # We post the voucher.
            self.write(cr, uid, [voucher.id], {
                'move_id': move_id,
                'state': 'posted',
                'number': name,
            })
            if voucher.journal_id.entry_posted:
                move_pool.post(cr, uid, [move_id], context={})
            # We automatically reconcile the account move lines.
            if len(wo_move_lines) == 0:
                reconcile = False
                for rec_ids in rec_list_ids:
                    if len(rec_ids) >= 2:
                        reconcile = move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=voucher.writeoff_acc_id.id, writeoff_period_id=voucher.period_id.id, writeoff_journal_id=voucher.journal_id.id)
        return True

account_voucher()

class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'

    def _check_amount(self, cr, uid, ids, context=None):
        today = time.strftime('%Y-%m-%d')
        for obj in self.browse(cr, uid, ids, context=context):
            if not obj.voucher_id: continue

            diff = abs(obj.amount) - obj.voucher_id.amount
            if obj.voucher_id:
                diff2 = 0.0
                for vl in obj.voucher_id.line_ids:
                    l_diff2 = 0.0
                    if vl.move_line_id and vl.move_line_id.cash_discount_date >= today:
                        l_diff2 = abs(vl.amount_original) * vl.move_line_id.cash_discount_rate
                    diff2 += l_diff2
                if abs(diff2 - diff) > 0.001: 
                    diff = 0.0
            if not self.pool.get('res.currency').is_zero(cr, uid, obj.statement_id.currency, diff):
                return False
        return True

    _columns = {
        'voucher_amount': fields.related('voucher_id', 'amount', type='float', string='Paid amount'),
    }

    _constraints = [
        (_check_amount, 'The amount of the voucher must be the same amount as the one on the statement line.', ['amount']),
    ]

account_bank_statement_line()
