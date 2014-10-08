# -*- coding: utf-8 -*-
#
#  File: wizard/wiz_acc_stmt_in_bnk_stmt.py
#  Module: ons_productivity_acc_stmt
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

import logging
_logger = logging.getLogger(__name__)

class wiz_acc_stmt_in_bnk_stmt(osv.osv_memory):
    _name = 'ons.wiz_acc_stmt_in_bnk_stmt'
    _description = 'Open-Net wizard: import account statements in a voucher'

    # ------------------------- Fields related
    
    _columns = {
        'journal_id': fields.many2one('account.journal', 'Journal'),
        'account_stmt_ids': fields.many2many('ons.account_statement', 'wiz_acc_stmt_in_bnk_stmt_rel', 'wiz_id', 'acc_stmt_id', 'Account statements' ),
    }
    
    _defaults = {
        'journal_id': lambda s,c,u,ct: ct.get('active_id', False) and s.pool.get('account.bank.statement').browse(c,u,ct['active_id'],context=ct).journal_id.id or False,
    }

    def _create_voucher_from_record(self, cr, uid, record,
                                    statement, line_ids, ttype, context=None):
        """Create a voucher with voucher line"""
        context.update({'move_line_ids': line_ids})
        voucher_obj = self.pool.get('account.voucher')
        move_line_obj = self.pool.get('account.move.line')
        voucher_line_obj = self.pool.get('account.voucher.line')
        line = move_line_obj.browse(cr, uid, line_ids[0])
        partner_id = line.partner_id and line.partner_id.id or False
        if not partner_id:
            return False
        move_id = line.move_id.id
        date = record['date'] or time.strftime('%Y-%m-%d')
        if ttype == 'receipt':
            account_id = statement.journal_id.default_debit_account_id and statement.journal_id.default_debit_account_id.id or False
        else:
            account_id = statement.journal_id.default_credit_account_id and statement.journal_id.default_credit_account_id.id or False
        voucher_res = {
                'type': ttype,
                'name': record['ref'],
                'partner_id': partner_id,
                'journal_id': statement.journal_id.id,
                'company_id': statement.company_id.id,
                'currency_id': statement.currency.id,
                'date': date,
                'amount': abs(record['amount']),
                'period_id': statement.period_id.id,
                'account_id': account_id,
            }

        voucher_id = voucher_obj.create(cr, uid, voucher_res, context=context)

        ctx = context.copy()
        ctx['move_line_ids'] = line_ids
        result = voucher_obj.recompute_voucher_lines(cr, uid, [], partner_id, statement.journal_id.id, record['amount'], False, ttype, date, context=context)
        voucher_line_dict = False
        if ttype == 'receipt':
            if result['value']['line_cr_ids']:
                for line_dict in result['value']['line_cr_ids']:
                    move_line = move_line_obj.browse(cr, uid, line_dict['move_line_id'], context)
                    if move_id == move_line.move_id.id:
                        voucher_line_dict = line_dict
        else:
            if result['value']['line_dr_ids']:
                for line_dict in result['value']['line_dr_ids']:
                    move_line = move_line_obj.browse(cr, uid, line_dict['move_line_id'], context)
                    if move_id == move_line.move_id.id:
                        voucher_line_dict = line_dict
        if voucher_line_dict:
            voucher_line_dict.update({'voucher_id': voucher_id})
            voucher_line_obj.create(cr, uid, voucher_line_dict, context=context)
        return voucher_id
    
    def do_it(self, cr, uid, ids, context=None):
        
        if not context:
            context = {}
        
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            #self.pool.get('ons.account_statement').import_mt940(cr, uid, False, f_content.split('\n'), context=context)

            inv_obj = self.pool.get('account.invoice')
            move_line_obj = self.pool.get('account.move.line')
            property_obj = self.pool.get('ir.property')
            statement_obj = self.pool.get('account.bank.statement')
            statement_line_obj = self.pool.get('account.bank.statement.line')
            statement_id = context.get('active_id', False)
            statement = statement_obj.browse(cr, uid, statement_id, context=context)

            for line in obj.account_stmt_ids:
                vals = {
                    'date': line.date_value,
                    'statement_id': statement_id, 
                }
                ref = ''
                obi = ''
                if not re.findall(r'[^0-9 ]+', line.dest):
                    if not re.findall(r'[^0-9 ]+', line.compl):
                        if len(line.dest) > len(line.compl):
                            ref = line.dest
                            obi = line.compl
                        else:
                            obi = line.dest
                            ref = line.compl
                    else:
                        ref = line.dest
                        obi = line.compl
                elif not re.findall(r'[^0-9 ]+', line.compl):
                    ref = line.compl
                    obi = line.dest
                elif line.dest.lower().strip() == 'nonref':
                    obi = line.compl
                    ref = '-'
                else:
                    obi = line.compl
                    ref = line.dest
                vals.update({
                    'name': obi,
                    'ref': ref
                })
                if line.op == 'C':
                    vals.update({
                        'type': 'customer',
                        'amount': line.amount,
                        'account_id': statement.journal_id.default_debit_account_id and statement.journal_id.default_debit_account_id.id or False,
                    })
                    ttype = 'receipt'
                    filter = [('journal_id.type','=','sale')]
                    acc_name = 'property_account_receivable'
                else:
                    vals.update({
                        'type': 'supplier',
                        'amount': -line.amount,
                        'account_id': statement.journal_id.default_credit_account_id and statement.journal_id.default_credit_account_id.id or False,
                    })
                    ttype = 'payment'
                    filter = [('journal_id.type','=','purchase')]
                    acc_name = 'property_account_payable'
                filter += [('reconcile_id', '=', False),('account_id.type', 'in', ['receivable', 'payable'])]
                line_ids = []
                if line.ref:
                    line_ids = move_line_obj.search(cr, uid, [('ref', 'ilike', line.ref)] + filter, order='date desc', context=context)
                    if line_ids:
                        vals.update({
                            'name': '/',
                            'ref': line.ref,
                        })
                        _logger.info(" ***** Found the account move line by line.ref")
                if not line_ids:
                    line_ids = move_line_obj.search(cr, uid, [('ref', '=', ref)] + filter, order='date desc', context=context)
                    if line_ids:
                        _logger.info(" ***** Found the account move line by ref")
                if not line_ids:
                    line_ids = move_line_obj.search(cr, uid, [('ref', '=', obi)] + filter, order='date desc', context=context)
                    if line_ids:
                        vals['name'] = ref
                        _logger.info(" ***** Found the account move line by obi")
                if not line_ids:
                    inv_ids = inv_obj.search(cr, uid, [('bvr_reference','=',ref),('state','=','open')], context=context)
                    if inv_ids:
                        move_ids = []
                        for inv in inv_obj.browse(cr, uid, inv_ids, context=context):
                            if inv.move_id:
                                move_ids.append(inv.move_id.id)
                        if move_ids:
                            line_ids = move_line_obj.search(cr, uid, [('move_id','in',move_ids)] + filter, order='date desc', context=context)
                
                if line_ids:
                    move_line = move_line_obj.browse(cr, uid, line_ids[0])

                    vals['account_id'] = move_line.account_id.id
                    if not vals['account_id']:
                        raise osv.except_osv(_('Error'),
                                         _('The properties account payable account receivable are not set'))
                
                    vals['partner_id'] = move_line.partner_id and move_line.partner_id.id or False
                    vals['voucher_id'] = self._create_voucher_from_record(cr, uid, vals,
                                                                        statement, line_ids, ttype,
                                                                        context=context)
                
                    statement_line_id = statement_line_obj.create(cr, uid, vals, context=context)
                    line.write({'reconciliation':statement_line_id, 'bank_statement_id':statement_id}, context=context)

        return {}

wiz_acc_stmt_in_bnk_stmt()
