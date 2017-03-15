# -*- coding: utf-8 -*-
#
# File: model/sale_crm.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api, _
from datetime import date


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    color = fields.Integer(string='Color Index')

    @api.model
    def view_header_get(self, view_id, view_type):
        if view_id != self.env.ref('ons_productivity_sale_crm.onsp_sale_crm_dashboard_view'):
            return False

        current_user = self.env.user
        if current_user.sale_team_id and current_user.sale_team_id.group_sale_target:
            header = _('Team Pipeline') + " - " + current_user.sale_team_id.name
        else:
            header = _('Pipeline Dashboard') + " - " + current_user.name

        return header

    @api.v7
    def retrieve_onsp_sales_dashboard(self, cr, uid, context=None):
        """
            Retrieves the values for the dashboard:
            personally invoiced or done by the whole team
        """

        res = self.retrieve_sales_dashboard(cr, uid, context=context)

        res.update({
            'invoiced': {'month':0, 'year':0},
            'planned': {'daily':0, 'month':0, 'year':0},
            'percent': {'month':0, 'daily':0},
        })

        # Determine if we're using the personnal or the group's invoicing target
        current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        uids = [uid]
        planned_total = current_user.yearly_planned_invoiced_amount
        if (context or {}).get('group_sale_target', False) and current_user.sale_team_id:
            if current_user.sale_team_id.member_ids:
                uids = [x.id for x in current_user.sale_team_id.member_ids]
            planned_total = current_user.sale_team_id.group_invoiced_planned

        # Invoiced this month
        account_invoice_domain = [
            ('state', 'in', ['open', 'paid']),
            ('date_invoice', '>=', date.today().replace(day=1)),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]
        if uids:
            account_invoice_domain.append(('user_id', 'in', uids))

        invoice_ids = self.pool.get('account.invoice').search_read(cr, uid, account_invoice_domain, ['amount_untaxed_signed'], context=context)
        for inv in invoice_ids:
            res['invoiced']['month'] += inv['amount_untaxed_signed']

        # Invoiced this year
        account_invoice_domain = [
            ('state', 'in', ['open', 'paid']),
            ('date_invoice', '>=', date.today().replace(day=1).replace(month=1)),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]
        if uids:
            account_invoice_domain.append(('user_id', 'in', uids))

        invoice_ids = self.pool.get('account.invoice').search_read(cr, uid, account_invoice_domain, ['amount_untaxed_signed'], context=context)
        for inv in invoice_ids:
            res['invoiced']['year'] += inv['amount_untaxed_signed']

        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)

        res.update({
            'planned': {
                'year': planned_total,
                'month': planned_total / 12,
                'daily': (planned_total / 365)* date.today().timetuple().tm_yday
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

    @api.model
    def action_open_pipeline_dashboard(self):
        """
            Handles the reaction to pipeline selection in the dashboard
        """

        ctx = self.env.context.copy()
        dom = []

        current_user = self.env.user

        # This will give the list of lead stages
        ctx['default_team_id'] = current_user.sale_team_id.id or False

        # Keep in context the kind of target: personal or sale team
        if current_user.sale_team_id.group_sale_target:
            ctx['group_sale_target'] = True

        if ctx.get('ons_search_for_the_team', False):
            # Jump to the team's leads/opportunities list
            action = self.env.ref('ons_productivity_sale_crm.crm_lead_action_activities')
            dom = [('user_id', 'in', [x.id for x in current_user.sale_team_id.member_ids])]
        else:
            # Jump to the personal dashboard
            action = self.env.ref('ons_productivity_sale_crm.onsp_sale_crm_dashboard_act')
            dom = [('user_id', '=', current_user.id)]

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': ctx,
            'res_model': action.res_model,
            'domain': dom
        }
        if  ctx.get('ons_search_for_the_team', False) and current_user.sale_team_id:
            result['name'] = current_user.sale_team_id.name


        return result
