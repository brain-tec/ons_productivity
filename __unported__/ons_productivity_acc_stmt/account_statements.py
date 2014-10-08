# -*- coding: utf-8 -*-
#
#  File: account_statements.py
#  Module: ons_cust_edsi_tech
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

from osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re
import glob
import os

import logging
_logger = logging.getLogger(__name__)

class account_statements( osv.osv ):
    _name = 'ons.account_statement'
    _description = 'Account statement'
    
    # ------------------------- Fields related
    
    _columns = {
        'name': fields.char( 'Name', size=64 ),
        'date_value': fields.date('Date value'),
        'date_acc': fields.date('Accounting date'),
        'op': fields.char('Operation', size=2),
        'amount': fields.float('Amount'),
        'dest': fields.char('Dest.', size=30),
        'compl': fields.text('Compl'),
        'ref': fields.text('Ref'),
        'reconciliation': fields.many2one('account.bank.statement.line', 'Statement line', ondelete='set null'),
        'bank_statement_id': fields.many2one('account.bank.statement', 'Bank statement'),
        'msg': fields.text('Message'),
    }
    
    _defaults = {
        'reconciliation': lambda *a: False,
    }
    
    _order = 'date_value desc'
    
    # ------------------------- Import handling
    
    def decode_mt940(self, cr, uid, f, ctx):
        # Returns a list of move lines, typically:
        # {
        #     'date': '2012-12-19', 
        #     'recs': [
        #         {'date_acc': '2012-12-19', 'dest': 'NONREF', 'compl': 'TEL. MOBILE A. RIZZO NOVEMBRE 2012', 'date_value': '2012-12-19', 'amount': 99.0, 'op': 'D', 'ref': 'blabla1'}, 
        #         {'date_acc': '2012-12-19', 'dest': 'NONREF', 'compl': 'TEL. MOBILE P. BONVIN NOV. 2012', 'date_value': '2012-12-19', 'amount': 106.15, 'op': 'D', 'ref': 'blabla2'}, 
        #         {'date_acc': '2012-12-19', 'dest': 'NONREF', 'compl': 'TEL. MOBILE J. GANDER OCT-NOV 2012', 'date_value': '2012-12-19', 'amount': 138.0, 'op': 'D', 'ref': 'blabla3'}, 
        #         {'date_acc': '2012-12-19', 'dest': 'NONREF', 'compl': 'DISQUES DUR SRV BACKUP', 'date_value': '121219', 'amount': 336.0, 'op': 'D', 'ref': 'blabla4'}
        #     ], 
        #     'amount': -1088.64,
        #     'op': 'C'
        # }
        # Please note:
        #   - the amount corresponds to the cumul before the records are handled
        #   - the 'ref' item corresponds to the last part of the :86: entry (spaces)
        #
    
    
        params = self.pool.get('ons.account_statement.params').get_instance(cr, uid, context=ctx)
        ref_mask = params and params.ref_mask or ''

        lst = []
        vals = {}
        lines = [line.strip() for line in f]
        i = 0
        max_i = len(lines) - 1
        while(i < max_i):
            l = lines[i]
    
            if l == '-}':
                if vals.get('recs'): lst += [vals]
                vals = {}
            
            if re.findall(r'^:20:XBS\/(\d{2})(\d{2})(\d{2}).+$', l):
                if vals.get('recs'): lst += [vals]
                vals = {
                    'date': re.sub(r'^:20:XBS\/(\d{2})(\d{2})(\d{2}).+$', r'20\1-\2-\3', l)
                }
    
                i += 1
                continue

            if re.findall(r'^:20:(\d{4})(\d{2})(\d{2}).+$', l):
                if vals.get('recs'): lst += [vals]
                vals = {
                    'date': re.sub(r'^:20:(\d{4})(\d{2})(\d{2}).+$', r'\1-\2-\3', l)
                }
    
                i += 1
                continue

            if not vals: 
                i += 1
                continue
            
            if re.findall(r'^:60F:C\d{6}CHF(\d+),(\d+)$', l):
                vals.update({
                    'amount': float(re.sub(r'^:60F:C\d{6}CHF(\d+),(\d+)$', r'\1.\2', l)),
                    'op': 'C',
                })
    
                i += 1
                continue
    
            if re.findall(r'^:60F:D\d{6}CHF(\d+),(\d+)$', l):
                vals.update({
                    'amount': float(re.sub(r'^:60F:D\d{6}CHF(\d+),(\d+)$', r'-\1.\2', l)),
                    'op': 'D',
                })
    
                i += 1
                continue
    
            if re.findall(r'^:61:\d{10}(C|D)(\d+),(\d{0,2})(.)(.{3})(.+)//.+$', l):
                _logger.debug(" ****** :61: handled: "+l)
                filter = r'^:61:(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(C|D)(\d+),(\d{0,2})(.)(.{3})(.+)//(.*)$' 
                rec = {
                    'date_value': '20' + re.sub(filter, r'\1', l) + '-' + re.sub(filter, r'\2', l) + '-' + re.sub(filter, r'\3', l),
                    'date_acc': '20' + re.sub(filter, r'\1', l) + '-' + re.sub(filter, r'\4', l) + '-' + re.sub(filter, r'\5', l),
                    'op': re.sub(filter, r'\6', l),
                    'amount': float(re.sub(filter, r'\7.\8', l)),
                    'dest': re.sub(filter, r'\9', l),
                    'name': re.sub(filter, r'\12', l),
                    'ref': '',
                }
                if rec['dest'] != 'NONREF':
                    rec['dest'] = re.sub(filter, r'\11', l)
                
                compl = ''
                i += 1
                while(i < max_i):
                    l2 = lines[i]
                    if re.findall(r'^:\d\d[MF]{0,1}:', l2):
                        l = l2
                        _logger.debug(" ****** :61: stopping with: "+l)
                        break
    
                    compl += l2
                    i += 1
    
                rec['compl'] = compl
                if not vals.get('recs',[]):
                    vals['recs'] = []
                vals['recs'] += [rec]
            else:
                _logger.debug(" ****** :61: skipped: "+l)
    
            if re.findall(r'^:86:.+\?(\d{2}).+$', l):
                _logger.debug(" ****** :86: handled by V1: "+l)
                i += 1
                ref = ''
                while(i < max_i):
                    l2 = lines[i]
                    if re.findall(r'^:\d\d[MF]{0,1}:', l2):
                        break
                    if l2[0:2] == '-}':
                        break
    
                    l += l2
                    i += 1
                    ref = l2.split(' ')[-1:]
    
                if not '?60' in l2:
                    continue
                
                rec['ref'] = ref
                rec['msg'] = l[4:]
                if not vals.get('recs',[]):
                    vals['recs'] = []
                _logger.debug(" ****** :86: new record by V1: "+str(rec))
                vals['recs'] += [rec]
    
                continue
            
            if re.findall(r'^:86:.+$', l):
                _logger.debug(" ****** :86: handled by V2: "+l)
                i += 1
                ref = ''
                while(i < max_i):
                    l2 = lines[i]
                    if re.findall(r'^:\d\d[MF]{0,1}:', l2):
                        break
                    if l2[0:2] == '-}':
                        break
    
                    l += l2
                    i += 1
                
                _logger.debug(' ****** :86: Searching for a reference in: "'+str(l)+'"')
                ref = ''
                if ref_mask:
                    check = re.compile(ref_mask).findall(l)
                    if check:
                        ref = check[0]
                else:
                    ref = l.split(' ')[-1:][0]
                rec['ref'] = ref
                rec['msg'] = l[4:]

                if not vals.get('recs',[]):
                    vals['recs'] = []
                _logger.debug(" ****** :86: new record by V2: "+str(rec))
                vals['recs'] += [rec]
    
                continue
            
            # default case: ignore
            i += 1
            _logger.debug(" ****** Ignored: "+l)
    
        if vals.get('recs'): lst += [vals]
        _logger.debug(" ****** Returning: "+str(lst))
        return lst
    
    def import_mt940(self, cr, uid, f_name, f_content, context={}):
        if f_name:
            f_content = open(f_name, 'r')
            if not f_content:
                raise osv.except_osv(_('Error !'), _("Can't read '%s'") % f_name)

        if not f_content:
            return False
        res = self.decode_mt940(cr, uid, f_content, context)
        
        for item in res:
            if not item.get('recs',[]): continue
            _logger.debug(" ******Importing MT940 records: found "+str(len(item['recs'])))
            for statment in item['recs']:
                if statment.get('ref'):
                    if self.search(cr, uid, [('ref','=',statment['ref'])], context=context):
                        _logger.debug(" ****** Already in the DB: ref='%s'" % (statment['ref'],))
                        continue
                if self.search(cr, uid, [('dest','=',statment['dest']), ('compl','=',statment['compl'])], context=context):
                    _logger.debug(" ****** Already in the DB: dest='%s' and compl='%s'" % (statment['dest'],statment['compl']))
                    continue
                new_id = self.create(cr, uid, statment, context=context)

        return True
    
    # ------------------------- Scheduler management
    
    def _create_voucher_from_record(self, cr, uid, record, statement, line_ids, ttype, context=None):
        """Create a voucher with voucher line"""
        context.update({'move_line_ids': line_ids})

        voucher_obj = self.pool.get('account.voucher')
        move_line_obj = self.pool.get('account.move.line')
        voucher_line_obj = self.pool.get('account.voucher.line')

        line = move_line_obj.browse(cr, uid, line_ids[0])
        partner_id = line.partner_id and line.partner_id.id or False
        if not partner_id:
            return False, False

        move_id = line.move_id.id
        result = voucher_obj.onchange_partner_id(cr, uid, [],
                                                 partner_id,
                                                 statement.journal_id.id,
                                                 abs(record['amount']),
                                                 statement.currency.id,
                                                 ttype,
                                                 statement.date,
                                                 context=context)
        voucher_res = {'type': ttype,
                       'name': record['ref'],
                       'partner_id': partner_id,
                       'journal_id': statement.journal_id.id,
                       'account_id': result.get('account_id', statement.journal_id.default_credit_account_id.id),
                       'company_id': statement.company_id.id,
                       'currency_id': statement.currency.id,
                       'date': record['date'] or time.strftime('%Y-%m-%d'),
                       'amount': abs(record['amount']),
                       'period_id': statement.period_id.id
                       }
        voucher_id = voucher_obj.create(cr, uid, voucher_res, context=context)

        voucher_line_dict = False
        if result['value']['line_cr_ids']:
            for line_dict in result['value']['line_cr_ids']:
                move_line = move_line_obj.browse(cr, uid, line_dict['move_line_id'], context)
                if move_id == move_line.move_id.id:
                    voucher_line_dict = line_dict
        voucher_line_id = False
        if voucher_line_dict:
            voucher_line_dict.update({
                'voucher_id': voucher_id,
                'amount': abs(record['amount']),
            })
            voucher_line_id = voucher_line_obj.create(cr, uid, voucher_line_dict, context=context)

        return voucher_id, voucher_line_id
    
    def handle_inputs(self, cr, uid, journal_id, account_code, context={}):
        _logger.info("Starting the management of account statement files")

        if not journal_id:
            _logger.info("Aborting: no journal ID")
            return False

        journal = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context)
        if not journal or not journal.default_debit_account_id:
            _logger.info("Aborting: no journal or no debit account in the journal")
            return False
        
        account_ids = self.pool.get('account.account').search(cr, uid, [('code','=', account_code)], context=context)
        if not account_ids:
            _logger.info("Aborting: no account code")
            return False
        account_id = account_ids[0]

        params = self.pool.get('ons.account_statement.params').get_instance(cr, uid, context=context)
        if not params or not params.directory_in or not params.file_name_mask:
            return False

        move_line_obj = self.pool.get('account.move.line')
        property_obj = self.pool.get('ir.property')
        statement_obj = self.pool.get('account.bank.statement')
        statement_line_obj = self.pool.get('account.bank.statement.line')
        
        # Determine the list of files to handle
        path = params.directory_in
        if path[-1:] != os.sep:
            path += os.sep
        path += params.file_name_mask
        ref = params.last_imported_file or ''
        for f_name in [x for x in glob.glob(path) if x > ref]:
            _logger.info("    handling " +str(f_name) )

            f_content = open(f_name, 'r')
            if not f_content:
                _logger.info("Error: can't open '%s'" % str(f_name))
                continue
            res = self.decode_mt940(cr, uid, f_content, context)
            f_content.close()
            
            # Loop on each bloc
            for item in res:
                # item is something like that:
                # {
                #     'date': '2013-02-08',
                #     'recs': [rec1, rec2, rec3] 
                # }
                if not item.get('recs',[]): continue
                statement = False
                statement_id = False
                validate_statement = False

                # Each bloc may contain more than one record
                for rec in item['recs']:
                    # rec is something like that:
                    # {
                    #     'date_acc': '2013-02-08', 
                    #     'name': '4BA0-0208-80-942', 
                    #     'dest': '010045886 942421', 
                    #     'compl': 'Rentrees de paiement BVRB', 
                    #     'date_value': '2013-02-08', 
                    #     'amount': 21.6, 
                    #     'op': 'C',
                    #     'ref' 'blabla'
                    # }
                    if rec['op'] != 'C':
                        continue
                    
                    voucher_id = False
                    voucher_line_id = False

                    # Prepare a bank statement line values
                    vals = {
                        'date': rec['date_value'],
                        'amount': rec['amount'],
                        'type': 'customer',
                        'account_id': account_id,
                    }
                    ref = ''
                    obi = ''
                    if not re.findall(r'[^0-9]+', rec['dest']):
                        ref = rec['dest']
                        obi = rec['compl']
                    elif not re.findall(r'[^0-9]+', rec['compl']):
                        ref = rec['compl']
                        obi = rec['dest']
                    elif rec['dest'].lower().strip() == 'nonref':
                        obi = rec['compl']
                        ref = '-'
                    else:
                        obi = rec['compl']
                        ref = rec['dest']
                    vals.update({
                        'name': obi,
                        'ref': ref
                    })

                    # Look fot the account move line(s) to handle
                    line_ids = []
                    if rec.get('ref', ''):
                        filter = [
                                    ('ref', '=', rec['ref']),
                                    ('reconcile_id', '=', False),
                                    ('account_id', '=', account_id)
                                ]
                        line_ids = move_line_obj.search(cr, uid, filter, order='date desc', context=context)
                    if not line_ids:
                        filter = [
                                    ('ref', '=', ref),
                                    ('reconcile_id', '=', False),
                                    ('account_id', '=', account_id)
                                ]
                        line_ids = move_line_obj.search(cr, uid, filter, order='date desc', context=context)
                    if not line_ids:
                        _logger.info(" Ref: %s - No account move line" % str(ref))
                        continue

                    # Setup the bank statement if needed
                    if not statement_id:
                        stm_vals = {
                            'journal_id': journal.id,
                        }
                        ctx = dict(context or {}, account_period_prefer_normal=True)
                        ctx['move_line_ids'] = line_ids
                        periods = self.pool.get('account.period').find(cr, uid, dt = item['date'], context=ctx)
                        if periods:
                            stm_vals['period_id'] = periods[0]
                        res = statement_obj.onchange_journal_id(cr, uid, statement_id, journal.id, context=context)
                        if res.get('value', {}):
                            stm_vals['balance_start'] = res['value']['balance_start']
                            stm_vals['currency'] = res['value']['currency']
                            if res['value']['company_id']:
                                stm_vals['company_id'] = res['value']['company_id'][0]
                        
                        statement_id = statement_obj.create(cr, uid, stm_vals, context=context)
                        if statement_id:
                            statement = statement_obj.browse(cr, uid, statement_id, context=context)
                    if not statement_id:
                        _logger.info(" Ref: %s - bank statement not created" % str(ref))
                        continue
                    
                    vals['statement_id'] = statement_id

                    # Add a new voucher + its line
                    voucher_id, voucher_line_id = self._create_voucher_from_record(cr, uid, vals, statement, line_ids, 'receipt', context=ctx)
                    if not voucher_id:
                        _logger.debug(" Ref: %s - partner not found on account move line" % str(ref))
                        continue
                    if not voucher_line_id:
                        _logger.debug(" Ref: %s - does not corresponds to a customer payment" % str(ref))
                        continue
                    vals['voucher_id'] = voucher_id
                    validate_statement = True
                    
                    # Add a new bank statement line
                    statement_line_id = statement_line_obj.create(cr, uid, vals, context=context)
                
                if validate_statement:
                    # Recompute the end total
                    statement = statement_obj.browse(cr, uid, statement_id, context=context)
                    tot = reduce(lambda x,y: x+y, [l.amount for l in statement.line_ids], statement.balance_start)
                    _logger.info("                      >>> Got "+str(tot))
                    statement.write({'balance_end_real': tot})

                    # This will reconcile the account move line as well
                    statement.button_confirm_bank()
        
        return True

account_statements()

class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    _columns = {
        'ons_account_statement_ids': fields.one2many('ons.account_statement', 'bank_statement_id', 'Account statements'),
    }

account_bank_statement()

class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'
    _columns = {
        'ons_account_statement_id': fields.one2many('ons.account_statement', 'reconciliation', 'Account statement'),
    }

account_bank_statement_line()
