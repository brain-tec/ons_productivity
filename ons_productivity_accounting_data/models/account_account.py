# -*- coding: utf-8 -*-
#  Copyright (c) 2018-TODAY Open-Net Ltd. All rights reserved.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class AccountAccount(models.Model):
    _inherit = 'account.account'

    def _get_account_type(self):
        self.ensure_one()

        '''
            Dict Struct:
            'type-name': {
                'limit': list of dicts as the keys 'min' (included) and 'max' (included) indicate the range
                'ref': ir.model.data ref,
                'en': english name, only used for search purposes on later time
                'fr': french name, only used for search porpeses on later time
            }
        '''

        dict_acc_types = {
            'liquidity': {
                'limit': [{'min': '1000','max': '1059'},],
                'ref': 'account.data_account_type_liquidity',
                'en': 'Bank and Cash', 'fr': 'Banque et liquidités',
            },
            'receivable': {
                'limit': [{'min': '1100','max': '1399'},],
                'ref': 'account.data_account_type_receivable',
                'reconcile': True,
                'en': 'Receivable', 'fr': 'Débiteurs',
            },
            'current_assets': {
                'limit': [
                    {'min': '1060','max': '1099'}, 
                    {'min': '1140','max': '1199'}, 
                    {'min': '1300','max': '1399'},
                ],
                'ref': 'account.data_account_type_current_assets',
                'en': 'Current Assets', 'fr': 'Actifs actuels',
            },
            'non_current_assets': {
                'limit': [
                    {'min': '1200','max': '1299'}, 
                    {'min': '1400','max': '1479'},
                    {'min': '1480','max': '1499'},
                ],
                'ref': 'account.data_account_type_non_current_assets',
                'en': 'Non-current Assets', 'fr': 'Actifs immobilisés',
            },
            'fixed_assets': {
                'limit': [
                    {'min': '1500','max': '1599'}, 
                    {'min': '1600','max': '1699'},
                    {'min': '1700','max': '1799'},
                ],
                'ref': 'account.data_account_type_fixed_assets',
                'en': 'Fixed Assets', 'fr': 'Immobilisations',
            },
            'payable': {
                'limit': [{'min': '2000','max': '2099'},],
                'ref': 'account.data_account_type_payable',
                'reconcile': True,
                'en': 'Payable', 'fr': 'Créanciers',
            },
            'liabilities': {
                'limit': [
                    {'min': '2100','max': '2199'}, 
                    {'min': '2200','max': '2299'},
                    {'min': '2300','max': '2399'},
                ],
                'ref': 'account.data_account_type_current_liabilities',
                'en': 'Current Liabilities', 'fr': 'Passif circulant / Passif à court terme',
            },
            'non_current_liabilities': {
                'limit': [
                    {'min': '2400','max': '2499'}, 
                    {'min': '2500','max': '2599'},
                    {'min': '2600','max': '2799'},
                ],
                'ref': 'account.data_account_type_non_current_liabilities',
                'en': 'Non-current Liabilities', 'fr': 'Passif immobilisé / Passif non-courants',
            },
            'equity': {
                'limit': [
                    {'min': '1800','max': '1999'}, 
                    {'min': '2800','max': '2899'},
                ],
                'ref': 'account.data_account_type_equity',
                'en': 'Equity', 'fr': 'Capitaux propes',
            },
            'earnings': {
                'limit': [{'min': '2900','max': '2991'},],
                'ref': 'account.data_unaffected_earnings',
                'en': 'Current Year Earnings', 'fr': "Bénéfices de l'année en cours",
            },
            'revenue': {
                'limit': [
                    {'min': '3000','max': '3899'},
                    {'min': '3900','max': '3999'},
                ],
                'ref': 'account.data_account_type_revenue',
                'en': 'Income', 'fr': 'Revenus',
            },
            'direct_costs': {
                'limit': [
                    {'min': '4000','max': '4999'},
                ],
                'ref': 'account.data_account_type_direct_costs',
                'en': 'Cost of Revenue', 'fr': 'Coût des ventes',
            },
            'depreciation': {
                'limit': [
                    {'min': '6800','max': '6899'},
                ],
                'ref': 'account.data_account_type_depreciation',
                'en': 'Depreciation', 'fr': 'Ammortissement',
            },
            'other_income': {
                'limit': [
                    {'min': '7000','max': '7999'},
                    {'min': '8000','max': '8499'},
                    {'min': '8500','max': '8899'},
                ],
                'ref': 'account.data_account_type_other_income',
                'en': 'Other Income', 'fr': 'Autres revenus',
            },
            'expenses': {
                'limit': [
                    {'min': '5000','max': '5999'},
                    {'min': '6000','max': '6799'},
                    {'min': '6900','max': '6999'},
                    {'min': '8900','max': '8999'},
                ],
                'ref': 'account.data_account_type_expenses',
                'en': 'Expenses', 'fr': 'Charges',
            },
        }

        acc_code = int(self.code)

        for acc_type in dict_acc_types:
            for limit in dict_acc_types[acc_type].get('limit'):
                if acc_code >= int(limit.get('min')) and acc_code <= int(limit.get('max')):
                    return self.env.ref(dict_acc_types[acc_type].get('ref')), True if dict_acc_types[acc_type].get('reconcile') else False
                else:
                    continue
        return False, False

    @api.multi
    def _onsp_fix_accounts_types(self):
        for account in self:
            acc_type, reconcile = account._get_account_type()
            if acc_type:
                account.reconcile = True if reconcile else False
                account.user_type_id = acc_type