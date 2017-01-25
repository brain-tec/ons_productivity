# -*- coding: utf-8 -*-
#
# File: model/sale_crm.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models
from datetime import date


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    color = fields.Integer(string='Color Index')

    def retrieve_onsp_sales_dashboard(self, cr, uid, context=None):

        res = self.retrieve_sales_dashboard(cr, uid, context=context)

        res.update({
            'invoiced': {'month':0, 'year':0},
            'planned': {'daily':0, 'month':0, 'year':0},
            'percent': {'month':0, 'daily':0},
        })

        # Invoiced this month
        account_invoice_domain = [
            ('state', 'in', ['open', 'paid']),
            ('user_id', '=', uid),
            ('date', '>=', date.today().replace(day=1)),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]

        invoice_ids = self.pool.get('account.invoice').search_read(cr, uid, account_invoice_domain, ['amount_untaxed_signed'], context=context)
        for inv in invoice_ids:
            res['invoiced']['month'] += inv['amount_untaxed_signed']

        # Invoiced this year
        account_invoice_domain = [
            ('state', 'in', ['open', 'paid']),
            ('user_id', '=', uid),
            ('date', '>=', date.today().replace(day=1).replace(month=1)),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]

        invoice_ids = self.pool.get('account.invoice').search_read(cr, uid, account_invoice_domain, ['amount_untaxed_signed'], context=context)
        for inv in invoice_ids:
            res['invoiced']['year'] += inv['amount_untaxed_signed']

        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)

        res.update({
            'planned': {
                'year': user.yearly_planned_invoiced_amount,
                'month': user.yearly_planned_invoiced_amount / 12,
                'daily': (user.yearly_planned_invoiced_amount / 365)* date.today().timetuple().tm_yday
            }
        })
        if not res['planned']['month']:
            res['percent']['month'] = 0
        else:
            diff = res['invoiced']['month'] - res['planned']['month']
            res['percent']['month'] = (diff / res['planned']['month']) * 100

        if not res['planned']['daily']:
            res['percent']['daily'] = 0
        else:
            diff = res['invoiced']['year'] - res['planned']['daily']
            res['percent']['daily'] = (diff / res['planned']['daily']) * 100

        return res
