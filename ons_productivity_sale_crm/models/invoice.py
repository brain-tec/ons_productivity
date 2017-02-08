# -*- coding: utf-8 -*-
#
# File: model/invoice.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api
import time


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def action_dashboard_open_invoices_list(self):
        """
            Handles the reaction to pipeline selection in the dashboard
        """

        invoices_filter = self.env.context.get('invoices_filter', '')
        dom = [
            ('type','=', 'out_invoice'),
            ('state', 'in', ['open', 'paid']),
        ]
        if invoices_filter == 'month':
            dom.append(('date','>=',time.strftime('%Y-%m-01')))
            dom.append(('date','<','2017-02-01'))
        else:
            dom.append(('date','>=',time.strftime('%Y-01-01')))

        current_user = self.env.user
        uids = [current_user.id]
        if current_user.sale_team_id and current_user.sale_team_id.group_sale_target:
            if invoices_filter == 'month':
                action = self.env.ref('ons_productivity_sale_crm.action_our_invoices_monthly')
            else:
                action = self.env.ref('ons_productivity_sale_crm.action_our_invoices_yearly')

            uids = [x.id for x in current_user.sale_team_id.member_ids]
            dom.append(('user_id','in',uids))
        else:
            if invoices_filter == 'month':
                action = self.env.ref('ons_productivity_sale_crm.action_my_invoices_monthly')
            else:
                action = self.env.ref('ons_productivity_sale_crm.action_my_invoices_yearly')

            dom.append(('user_id','=',uid))

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': self.env.context,
            'res_model': action.res_model,
            'domain': dom
        }

        return result
