# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_test_reconciliations
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
##############################################################################
#    
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################


from openerp import models, api


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def reconciliation_widget_preprocess(self):
        """ Get statement lines of the specified statements or all unreconciled statement lines and try to automatically reconcile them / find them a partner.
            Return ids of statement lines left to reconcile and other data for the reconciliation widget.
        """
        statements = self
        bsl_obj = self.env['account.bank.statement.line']

        # NB : The field account_id can be used at the statement line creation/import to avoid the reconciliation process on it later on,
        # this is why we filter out statements lines where account_id is set
        st_lines_filter = [('journal_entry_ids', '=', False), ('account_id', '=', False)]
        if statements:
            st_lines_filter += [('statement_id', 'in', statements.ids)]

        # Try to automatically reconcile statement lines
        automatic_reconciliation_entries = []
        st_lines_left = self.env['account.bank.statement.line']
        for st_line in bsl_obj.search(st_lines_filter):
            st_lines_left = (st_lines_left | st_line)
#             res = st_line.auto_reconcile()
#             if not res:
#                 st_lines_left = (st_lines_left | st_line)
#             else:
#                 automatic_reconciliation_entries.append(res.ids)

        # Try to set statement line's partner
        for st_line in st_lines_left:
            if st_line.name and not st_line.partner_id:
                additional_domain = [('ref', '=', st_line.name)]
                match_recs = st_line.get_move_lines_for_reconciliation(limit=1, additional_domain=additional_domain, overlook_partner=True)
                if match_recs and match_recs[0].partner_id:
                    st_line.write({'partner_id': match_recs[0].partner_id.id})

        # Collect various informations for the reconciliation widget
        notifications = []
        num_auto_reconciled = len(automatic_reconciliation_entries)
        if num_auto_reconciled > 0:
            auto_reconciled_message = num_auto_reconciled > 1 \
                and _("%d transactions were automatically reconciled.") % num_auto_reconciled \
                or _("1 transaction was automatically reconciled.")
            notifications += [{
                'type': 'info',
                'message': auto_reconciled_message,
                'details': {
                    'name': _("Automatically reconciled items"),
                    'model': 'account.move',
                    'ids': automatic_reconciliation_entries
                }
            }]

        lines = []
        for el in statements:
            lines.extend(el.line_ids.ids)
        lines = list(set(lines))

        return {
            'st_lines_ids': st_lines_left.ids,
            'notifications': notifications,
            'statement_name': len(statements) == 1 and statements[0].name or False,
            'num_already_reconciled_lines': statements and bsl_obj.search_count([('journal_entry_ids', '!=', False), ('id', 'in', lines)]) or 0,
        }
