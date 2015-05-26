# -*- coding: utf-8 -*-
#
#  File: wizard/wiz_end_repair.py
#  Module: ons_productivity_stock
#
#  Created by cyp@open-net.ch
#  Original code by CampToCamp SA 2008
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
##############################################################################
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time

import logging
_logger = logging.getLogger(__name__)

from tools.misc import UpdateableStr
FORM = UpdateableStr()
#
# TODO: check unit of measure !!!
#
class onsp_wizard_scan_bvr(osv.osv_memory):
    _name = 'onsp.wiz.scan_bvr'
    _description = 'Open-Net wizard: BVR scan'
    
    # ------------------------- Fields management

    _columns = {
        # Base fields, always needed
        'bvr_string': fields.char('BVR string', size=128, required=True, help="""The line at the bottom right\nof the BVR"""),
        'journal_id': fields.many2one('account.journal', 'Journal', required=True, domain=[('type','in',['purchase'])]),

        # Complementary fields, should be filled automatically if anything goes right
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, help="""The supplier who send the invoice.\nIf it is not set you have to create it"""),
        'account_id': fields.many2one('res.partner.bank', 'Partner bank account', required=True, help="""The bank account of the supplier.\nIf it is not set you have to create it"""),
    }
    
    # ------------------------- Interface related
        
    def on_change_bvr_string(self, cr, uid, ids, bvr_str):
        vals = {
            'partner_id': False,
            'account_id': False,
        }
        bvr_struct = self._get_bvr_structurated(bvr_str)
        if bvr_struct:
            partner_bank_obj = self.pool.get('res.partner.bank')
            searched_partner_bank = partner_bank_obj.search(cr, uid, [('acc_number', '=',bvr_struct[bvr_struct['domain']])])
            if searched_partner_bank:
                partner_bank = partner_bank_obj.browse(cr, uid, searched_partner_bank[0])
                if partner_bank:
                    vals = {
                        'partner_id': partner_bank.partner_id.id,
                        'account_id': partner_bank.id,
                    }
        
        return {'value': vals}
    
    def on_change_partner(self, cr, uid, ids, partner_id):
        partner_bank_obj = self.pool.get('res.partner.bank')
        searched_partner_bank = partner_bank_obj.search(cr, uid, [('partner_id', '=',partner_id)])
        vals = {
            'account_id': searched_partner_bank and searched_partner_bank[0] or False,
        }
        
        return {'value': vals}
    
    def do_create_invoice(self, cr, uid, ids, context={}):
        datas = self.read(cr, uid, ids[0], context=context)
        if not datas: return False
        
        return self._create_direct_invoice(cr, uid, datas, context=context)
    
    # ------------------------- Tools

    def _check_number(self,part_validation):
        nTab = [0, 9, 4, 6, 8, 2, 7, 1, 3, 5]
        resultnumber = 0;
        for number in part_validation:
            resultnumber = nTab[(resultnumber + int(number) - 0) % 10]
        return (10 - resultnumber) % 10

    def _get_invoice_address(self, cr, uid, partner_id):
        partner_obj = self.pool.get('res.partner')
        addresses = partner_obj.address_get(cr, uid, [partner_id], ['invoice'])
        adr_id = addresses and addresses.get('invoice', addresses.get('default', False)) or False
        if not adr_id:
            raise osv.except_osv(_('Address Error'), _('No Address Assign to this partner'))
        return adr_id

    def _construct_bvrplus_in_chf(self,bvr_string):
        if len(bvr_string) <> 43:
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error Première partie'))
        if self._check_number(bvr_string[0:2]) <> int(bvr_string[2]):
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error Deuxième partie'))
        if self._check_number(bvr_string[4:30]) <> int(bvr_string[30]):
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error troisème partie'))
        if self._check_number(bvr_string[33:41]) <> int(bvr_string[41]):
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error 4 partie'))
        
        bvr_struct = {
                'type' : bvr_string[0:2],
                'amount' : 0.0,
                'reference' : bvr_string[4:31],
                'bvrnumber' : bvr_string[4:10],
                'beneficiaire' : self._create_bvr_account(bvr_string[33:42]),
                'domain' : 'beneficiaire',
                'currency' : ''
            }

        return bvr_struct
        
    def _construct_bvr_in_chf(self,bvr_string):
        if len(bvr_string) <> 53:
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error Première partie'))
        if self._check_number(bvr_string[0:12]) <> int(bvr_string[12]):
            raise osv.except_osv(_('AccountError'), _('BVR CheckSum Error Deuxième partie'))
        if self._check_number(bvr_string[14:40]) <> int(bvr_string[40]):
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error troisème partie'))
        if self._check_number(bvr_string[43:51]) <> int(bvr_string[51]):
            raise osv.except_osv(_('AccountError'), _('BVR CheckSum Error 4 partie'))
        
        bvr_struct = {
                'type' : bvr_string[0:2],
                'amount' : float(bvr_string[2:12])/100,
                'reference' : bvr_string[14:41],
                'bvrnumber' : bvr_string[14:20],
                'beneficiaire' : self._create_bvr_account(bvr_string[43:52]),
                'domain' : 'beneficiaire',
                'currency' : ''
            }

        return bvr_struct

    def _construct_bvr_postal_in_chf(self,bvr_string):
        if len(bvr_string) <> 42:
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error Première partie'))

        bvr_struct = {
                'type' : bvr_string[0:2],
                'amount' : float(bvr_string[2:12])/100,
                'reference' : bvr_string[14:30],
                'bvrnumber' : '',
                'beneficiaire' : self._create_bvr_account(bvr_string[32:41]),
                'domain' : 'beneficiaire',
                'currency' : ''
            }
        
        return bvr_struct

    def _construct_bvr_postal_other_in_chf(self,bvr_string):
        if len(bvr_string) <> 41:
            raise osv.except_osv(_('Account Error'), _('BVR CheckSum Error Première partie'))

        bvr_struct = {
                'type' : bvr_string[0:2],
                'amount' : float(bvr_string[7:16])/100,
                'reference' : bvr_string[18:33],
                'bvrnumber' : '000000',
                'beneficiaire' : self._create_bvr_account(bvr_string[34:40]),
                'domain' : 'beneficiaire',
                'currency' : ''
            }
        
        return bvr_struct
    
    def _create_direct_invoice(self, cr, uid, data, context):
        if data['account_id']:
            account_info = self.pool.get('res.partner.bank').browse(cr,uid,data['account_id'][0])
        
        bvr_struct = self._get_bvr_structurated(data['bvr_string'])

        ## We will now search the currency_id
        #
        
        #
        currency_search = self.pool.get('res.currency').search(cr,uid,[('name', '=',bvr_struct['currency'])])
        currency_id = self.pool.get('res.currency').browse(cr,uid,currency_search[0])

        ## Account Modification     TODO?
        #self.pool.get('res.partner.bank').write(cr,uid,data['account_id'][0],{'acc_number': bvr_struct[bvr_struct['domain']]})
        date_due = time.strftime('%Y-%m-%d')

        # We will now compute the due date and fixe the payment term
        payment_term_id = account_info.partner_id.property_payment_term and account_info.partner_id.property_payment_term.id or False
        if payment_term_id:
            #We Calculate due_date
            res = self.pool.get('account.invoice').onchange_payment_term_date_invoice(cr,uid,[],payment_term_id,time.strftime('%Y-%m-%d'))
            date_due = res['value']['date_due']
        ##
        #
        valid_types = { 'purchase':'in_invoice','sale':'out_invoice'}
        journal = self.pool.get('account.journal').browse(cr, uid, data['journal_id'][0], context=context)
        inv_type = valid_types.get(journal.type, False)
        if not inv_type:
            raise osv.except_osv(_('Journal Type Error'), _('Invalid journal selected: must be for purchases or sales!'))
        if inv_type == 'in_invoice':
            account_id = account_info.partner_id.property_account_payable.id
        else:
            account_id = account_info.partner_id.property_account_receivable.id
        curr_invoice = {
                'name': time.strftime('%Y-%m-%d'),
                'partner_id': account_info.partner_id.id,
                'address_invoice_id': self._get_invoice_address(cr,uid,account_info.partner_id.id),
                'account_id': account_id,
                'date_due': date_due,
                'date_invoice': time.strftime('%Y-%m-%d'),
                'payment_term': payment_term_id,
                'reference_type': 'bvr',
                'reference' :  bvr_struct['reference'],
                'amount_total' :  bvr_struct['amount'],
                'check_total' :  bvr_struct['amount'],
                'partner_bank_id' : account_info.id,
                'comment': '',
                'currency_id': currency_id.id,
                'journal_id' :  journal.id,
                'type': inv_type,
            }
        
        last_invoice = self.pool.get('account.invoice').create(cr, uid, curr_invoice)
        invoices = []
        invoices.append(last_invoice)

        view_name = { 'in_invoice': 'account.invoice.supplier.form', 'out_invoice':'account.invoice.form' }[inv_type]
        cr.execute('select id,name from ir_ui_view where model=%s and name=%s', ('account.invoice', view_name))
        view_res = cr.fetchone()

        journal_type = { 'in_invoice': 'purchase', 'out_invoice': 'sale' }[inv_type]

        return {
            'domain': "[('id','in', ["+','.join(map(str,invoices))+"])]",
            'name': 'Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            #'view_id': view_res,
            'context': "{'type':'%s', 'journal_type':'%s'}" % (inv_type,journal_type),
            'type': 'ir.actions.act_window',
            'res_id':invoices
        }
 
    def _create_bvr_account(self,account_unformated):
        account_formated = account_unformated[0:2] + '-' + str(int(account_unformated[2:len(account_unformated)-1])) + '-' +  account_unformated[len(account_unformated)-1:len(account_unformated)]
        
        return account_formated
    
    def _get_bvr_structurated(self,bvr_string):
        if not bvr_string: return False

        ## We will get the 2 frist digit of the BVr string in order
        ## to now the BVR type of this account
        bvr_type = bvr_string[0:2]
        if bvr_type == '01' and len(bvr_string) == 42:
            ## This BVr is the type of BVR in CHF
            # WE will call the function and Call
            

            bvr_struct =  self._construct_bvr_postal_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number if not we 
            ## will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'CHF'
            a=b1
        ##
        elif bvr_type == '01':
            ## This BVr is the type of BVR in CHF
            # WE will call the function and Call
            bvr_struct =  self._construct_bvr_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number if not 
            ## we will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'CHF'
        ##
        elif bvr_type == '03':
            ## It will be (At this time) the same work 
            ## as for a standard BVR with 01 code
            bvr_struct =  self._construct_bvr_postal_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number 
            ## if not we will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'CHF'
        ##
        elif bvr_type == '04':
            ## It the BVR postal in CHF
            bvr_struct =  self._construct_bvrplus_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number
            ## if not we will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'CHF'
        ##
        elif bvr_type == '21':
            ## It for a BVR in Euro
            bvr_struct =  self._construct_bvr_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number if 
            ## not we will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'EUR'
        ##
        elif bvr_type == '31':
            ## It the BVR postal in CHF
            bvr_struct =  self._construct_bvrplus_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number if not 
            ## we will make the search of the account base on
            ##his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'EUR'

        elif bvr_type[0:1] == '<' and len(bvr_string) == 41:
            ## It the BVR postal in CHF
            
            bvr_struct =  self._construct_bvr_postal_other_in_chf(bvr_string)
            ## We will test if the BVR have an Adherent Number 
            ## if not we will make the search of the account base on
            ## his name non base on the BVR adherent number
#             if (bvr_struct['bvrnumber'] == '000000'):
#                 bvr_struct['domain'] = 'name'
#             else:
#                 bvr_struct['domain'] = 'bvr_adherent_num'
            ## We will set the currency , in this case it's allways CHF
            bvr_struct['currency'] = 'CHF'

        ##
        ##            
        else:
            raise osv.except_osv(_('BVR Type error'), _('This kind of BVR is not supported at this time'))
        return bvr_struct
        
    def _validate_account(self, cr, uid, data, context):
        # BVR Standrard
        #0100003949753>120000000000234478943216899+ 010001628>
        # BVR without BVr Reference
        #0100000229509>000000013052001000111870316+ 010618955>
        # BVR + In CHF
        #042>904370000000000000007078109+ 010037882>
        # BVR In euro
        #2100000440001>961116900000006600000009284+ 030001625>
        #<060001000313795> 110880150449186+ 43435>
        #<010001000165865> 951050156515104+ 43435>
        #<010001000060190> 052550152684006+ 43435>
        # Exemples TSE:
        # 0100000158305>000000000477960700004692148+ 010496631>
        # 0100000080504>000924738899018808000920133+ 010230504>
        valid_types = { 'purchase':'in_invoice','sale':'out_invoice'}
        journal = self.pool.get('account.journal').browse(cr, uid, data['journal_id'][0], context=context)
        inv_type = valid_types.get(journal.type, False)
        if not inv_type:
            raise osv.except_osv(_('Journal Type Error'), _('Invalid journal selected: must be for purchases or sales!'))

        #pool = pooler.get_pool(cr.dbname)
        ##

        # Explode and check  the BVR Number and structurate it
        ##
        bvr_struct = self._get_bvr_structurated(data['bvr_string'])

        ## We will now search the account linked with this BVR
        vals = {}
        partner_bank_obj = self.pool.get('res.partner.bank')
        partner_bank_search = partner_bank_obj.search(cr, uid, [('acc_number', '=',bvr_struct[bvr_struct['domain']])])
        if partner_bank_search:
            # we have found the account corresponding to the bvr_adhreent_number
            # so we can directly create the account
            # 
            partner_bank_result = partner_bank_obj.browse(cr, uid, partner_bank_search[0])
            vals['account_id'] = partner_bank_result.id

        # we haven't found a valid bvr_adherent_number
        # we will need to create or update 
        #
        return {'value': vals}
         
    def _validate_journal(self, cr, uid, data, context):
        valid_types = { 'purchase':'in_invoice','sale':'out_invoice'}
        journal = self.pool.get('account.journal').browse(cr, uid, data['journal_id'][0], context=context)
        inv_type = valid_types.get(journal.type, False)
        if not inv_type:
            raise osv.except_osv(_('Journal Type Error'), _('Invalid journal selected: must be for purchases or sales!'))
        
        return 'create'

onsp_wizard_scan_bvr()
