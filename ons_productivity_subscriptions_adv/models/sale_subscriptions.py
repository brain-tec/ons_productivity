# -*- coding: utf-8 -*-
#
#  File: models/sale_subscriptions.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################


from openerp.osv import osv, fields
import openerp.tools as tools
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class SaleSubscription(osv.osv):
    _inherit = 'sale.subscription'

    # ---------- Fields management

    def _comp_next_date(self, cr, uid, ids, fieldnames, args, context=None):
        result = dict.fromkeys(ids, False)

        current_date = datetime.now()
        s_current_date = current_date.strftime('%Y-%m-%d')

        for contract in self.browse(cr, uid, ids, context=context):
            min_date = False
            for line in contract.recurring_invoice_line_ids:
                if not line.is_active or \
                    not line.is_billable or \
                    not line.recurring_rule_type or \
                    line.recurring_rule_type == 'none' or \
                    not line.recurring_rule_type or \
                    not line.recurring_next_date:

                    continue

                next = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                if context.get('force_date', False):
                    before = next
                else:
                    before = (next - relativedelta(days=(line.cancellation_deadline or 0))).strftime('%Y-%m-%d')
                if not min_date:
                    min_date = before
                    continue
                if before > min_date:
                    continue
                min_date = before
            result[contract.id] = min_date

        return result

    def _get_active_lines(self, cr, uid, ids, context=None):
        result = []
        for line in self.pool.get('sale.subscription.line').browse(cr, uid, ids, context=context):
            if line.is_active:
                result.append(line.analytic_account_id.id)
        return result

    def _get_sales_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        SaleSubscription = self.pool.get('sale.order')
        for subscr in self.browse(cr, uid, ids, context=context):
            res[subscr.id] = len(SaleSubscription.search(cr, uid, [('subscription_id','=',subscr.id)], context=context))
        return res

    def _get_invoices_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        InvoiceSubscription = self.pool.get('account.invoice')
        for subscr in self.browse(cr, uid, ids, context=context):
            res[subscr.id] = len(InvoiceSubscription.search(cr, uid, [('subscription_id','=',subscr.id)], context=context))
        return res

    def _get_non_recurring_line_ids(self, cr, uid, ids, context=None):
        result = []
        for line in self.pool.get('sale.subscription.line').browse(cr, uid, ids, context=context):
            if line.is_active and (not line.recurring_rule_type or line.recurring_rule_type == 'none'):
                result.append(line.analytic_account_id.id)
        return result

    def _get_non_recurring_price(self, cr, uid, ids, fieldnames, args, context=None):
        result = dict.fromkeys(ids, 0.0)
        for account in self.browse(cr, uid, ids, context=context):
            result[account.id] = sum(line.price_subtotal
                                     for line in account.recurring_invoice_line_ids
                                     if line.is_active and (not line.recurring_rule_type or line.recurring_rule_type == 'none'))
        return result

    def _get_recurring_line_ids(self, cr, uid, ids, context=None):
        result = []
        for line in self.pool.get('sale.subscription.line').browse(cr, uid, ids, context=context):
            if line.is_active and line.recurring_rule_type and line.recurring_rule_type != 'none':
                result.append(line.analytic_account_id.id)
        return result

    def _get_recurring_price(self, cr, uid, ids, fieldnames, args, context=None):
        result = dict.fromkeys(ids, 0.0)
        for account in self.browse(cr, uid, ids, context=context):
            result[account.id] = sum(line.price_subtotal
                                     for line in account.recurring_invoice_line_ids
                                     if line.is_active and line.recurring_rule_type and line.recurring_rule_type != 'none' and line.is_active)
        return result

    _columns = {
        'recurring_rule_type': fields.selection([
                ('daily', 'Day(s)'),
                ('weekly', 'Week(s)'),
                ('monthly', 'Month(s)'),
                ('yearly', 'Year(s)')
            ],
            'Recurrency',
            help="Invoice automatically repeat at specified interval",
            readonly=True
        ),
        'recurring_interval': fields.integer('Repeat Every', help="Repeat every (Days/Week/Month/Year)", readonly=True),
        'recurring_next_date': fields.function(
            _comp_next_date,
            string='Date of Next Invoice',
            type='date',
            store={
                'sale.subscription.line': (_get_active_lines, ['recurring_next_date','cancellation_deadline', 'is_active'], 5)
            }
        ),
        'recurring_generates': fields.selection([
                ('invoice', 'An invoice'),
                ('sale', 'A sale'),
            ],
            'Generates',
            default='invoice'
        ),
        'sales_count': fields.function(
            _get_sales_count,
            string='Sales count',
            type='integer'
        ),
        'invoices_count': fields.function(
            _get_invoices_count,
            string='Invoices count',
            type='integer'
        ),
        'non_recurring_total': fields.function(
            _get_non_recurring_price,
            string="Non-recurring Price",
            type="float",
            store={
               'account.analytic.account': (lambda s, cr, uid, ids, c={}: ids, ['recurring_invoice_line_ids'], 5),
               'sale.subscription.line': (_get_non_recurring_line_ids,
                                          ['product_id', 'quantity', 'actual_quantity', 'sold_quantity', 'uom_id',
                                           'price_unit', 'discount', 'price_subtotal', 'is_active'],
                                          5),
            },
            track_visibility='onchange'),
        'recurring_total': fields.function(
            _get_recurring_price,
            string="Recurring Price",
            type="float",
            store={
                'account.analytic.account': (lambda s, cr, uid, ids, c={}: ids, ['recurring_invoice_line_ids'], 5),
                'sale.subscription.line': (_get_recurring_line_ids,
                                           ['product_id', 'quantity', 'actual_quantity', 'sold_quantity', 'uom_id',
                                            'price_unit', 'discount', 'price_subtotal', 'is_active'],
                                           5),
        }, track_visibility='onchange'),
    }

    _defaults = {
        'recurring_rule_type': lambda *a: 'daily',
        'recurring_interval': lambda *a: 1,
    }

    # ---------- Instances management

    def create(self, cr, uid, vals, context={}):
        date_start = vals.get('date_start', False)

        new_id = super(SaleSubscription, self).create(cr, uid, vals, context=context)

        if new_id and date_start:
            self.update_lines_date_start(cr, uid, [new_id], date_start, context=context)

        return new_id

    def write(self, cr, uid, ids, vals, context={}):
        date_start = vals.get('date_start', False)

        ret = super(SaleSubscription, self).write(cr, uid, ids, vals, context=context)

        if date_start:
            self.update_lines_date_start(cr, uid, ids, date_start, context=context)

        return ret

    # ---------- UI management

    def on_change_template(self, cr, uid, ids, template_id, date_start=False, context=None):
        res = super(SaleSubscription, self).on_change_template(cr, uid, ids, template_id, context=context)
        if not template_id:
            return res
        if 'date_start' in res['value']:
            del res['value']['date_start']
        if not date_start:
            res['value']['date_start'] = datetime.now()

        template = self.browse(cr, uid, template_id, context=context)
        if template and template.recurring_generates:
            res['value']['recurring_generates'] = template.recurring_generates

        ProductProduct = self.pool.get('product.product')
        ctx = (context or {}).copy()
        if res['value'].get('pricelist_id', False):
            ctx['pricelist'] = res['value']['pricelist_id']

        invoice_line_ids = []
        for x in template.recurring_invoice_line_ids:

            line_item = {
                'product_id': x.product_id.id,
                'uom_id': x.uom_id.id,
                'name': x.name,
                'sold_quantity': x.quantity,
                'price_unit': x.price_unit or 0.0,
                'analytic_account_id': x.analytic_account_id and x.analytic_account_id.id or False,
                'recurring_rule_type': 'none',
                'recurring_interval': 1,
                'recurring_next_date': None,
                'is_active': x.is_active,
                'is_billable': x.is_billable,
                'sequence': x.sequence,
                'cancellation_deadline': x.cancellation_deadline
            }

            if x.recurring_rule_type and x.recurring_rule_type != 'none':
                next_date = datetime.now()
                if date_start:
                    next_date = datetime.strptime(date_start, '%Y-%m-%d')
                    line_item.update({
                        'recurring_rule_type': x.recurring_rule_type,
                        'recurring_interval': x.recurring_interval,
                        'recurring_next_date': next_date
                    })
            invoice_line_ids.append((0, 0, line_item))
        res['value']['recurring_invoice_line_ids'] = invoice_line_ids

        return res

    # Show the list of corresponding invoices
    def action_subscription_invoice(self, cr, uid, ids, context=None):
        subs = self.browse(cr, uid, ids, context=context)
        invoice_ids = self.pool['account.invoice'].search(cr, uid, [('subscription_id', 'in', [x.id for x in subs])], context=context)
        imd = self.pool['ir.model.data']
        list_view_id = imd.xmlid_to_res_id(cr, uid, 'account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id(cr, uid, 'account.invoice_form')
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.invoice",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["id", "in", invoice_ids]],
            "context": {"create": False},
            "name": _("Invoices"),
        }

    # Show the list of corresponding sales
    def action_subscription_sale(self, cr, uid, ids, context=None):
        subs = self.browse(cr, uid, ids, context=context)
        analytic_ids = [sub.analytic_account_id.id for sub in subs]
        sale_ids = self.pool['sale.order'].search(cr, uid, [('subscription_id', 'in', [x.id for x in subs])], context=context)
        imd = self.pool['ir.model.data']
        list_view_id = imd.xmlid_to_res_id(cr, uid, 'sale.view_order_tree')
        form_view_id = imd.xmlid_to_res_id(cr, uid, 'ons_productivity_subscriptions_adv.onsp_view_sale_order_subscription_form')
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["id", "in", sale_ids]],
            "context": {"create": False},
            "name": _("Sales"),
        }

    # Generate an invoice/a sale
    def action_recurring_invoice(self, cr, uid, ids, context=None):
        return self._recurring_create_invoice(cr, uid, ids, context=context)

    # ---------- Utils

    def update_lines_date_start(self, cr, uid, ids, new_date_start, context={}):
        SaleSubscriptionLines = self.pool.get('sale.subscription.line')
        lines = SaleSubscriptionLines.search(cr, uid, [('analytic_account_id','in', ids),('recurring_rule_type','!=','none')], context=context)
        if lines:
            ctx = context.copy()
            ctx['force_date'] = new_date_start
            SaleSubscriptionLines.write(cr, uid, lines, {'recurring_next_date': new_date_start}, context=ctx)

        return True

    def get_lang_dict(self, cr, uid, context={}):
        pool_lang = self.pool.get('res.lang')
        lang = context.get('lang', 'en_US') or 'en_US'
        lang_ids = pool_lang.search(cr, uid,[('code','=',lang)])[0]
        lang_obj = pool_lang.browse(cr,uid,lang_ids)

        return {'lang_obj':lang_obj,'date_format':lang_obj.date_format,'time_format':lang_obj.time_format}

    def recurring_invoice(self, cr, uid, ids, context=None):
        return self._recurring_create_invoice(cr, uid, ids, context=context)

    def _prepare_invoice_line(self, cr, uid, line, fiscal_position, context={}):
        values = super(SaleSubscription, self)._prepare_invoice_line(cr, uid, line, fiscal_position, context=context)
        if not line.is_billable:
            values['price_unit'] = 0

        return values

    def _prepare_invoice_lines(self, cr, uid, contract, fiscal_position_id, context={}):
        invoice_lines = []
        fpos_obj = self.pool.get('account.fiscal.position')
        fiscal_position = None
        if fiscal_position_id:
            fiscal_position = fpos_obj.browse(cr, uid, fiscal_position_id, context=context)
        lang_dict = self.get_lang_dict(cr, uid, context=context)
        date_format = lang_dict['date_format']

        s_current_date = fields.date.context_today(self, cr, uid)

        for line in contract.recurring_invoice_line_ids:
            if (line.recurring_rule_type or '') != 'none':
                if not line.recurring_next_date or not line.is_active:
                    continue
                line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d') - \
                    relativedelta(days=(line.cancellation_deadline))
                s_line_date = line_date.strftime('%Y-%m-%d')
                if s_current_date < s_line_date:
                    continue
            else:
                if not line.is_active:
                    continue
                if line.recurring_next_date:
                    line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                    s_line_date = line_date.strftime('%Y-%m-%d')
                    if s_current_date != s_line_date:
                        continue

            values = self._prepare_invoice_line(cr, uid, line, fiscal_position, context=context)

            # Overwrite sale_contract_asset's default asset handling:
            #   the info is now computed from the line's recurrence
            #   it defaults from the product if empty
            month = 0
            asset_cat = False
            if line.recurring_rule_type in ('dayly','weekly'):
                month = 0   # i.e. not actually supported
            elif line.recurring_rule_type == 'monthly':
                month = line.recurring_interval
            elif line.recurring_rule_type == 'yearly':
                month = 12
            if month:
                asset_cat = self.env['account.asset.category'].search([('type','=','sale'),('active','=',True),('method_number','=',month)])
                if asset_cat:
                    asset_cat = asset_cat[0].id
                else:
                    asset_cat = False
            if not asset_cat and line.product_id.product_tmpl_id.deferred_revenue_category_id:
                asset_cat = line.product_id.product_tmpl_id.deferred_revenue_category_id
                if asset_cat:
                    if asset_cat.account_asset_id:
                        values['account_id'] = asset_cat.account_asset_id.id
                    asset_cat = asset_cat.id

            values['asset_category_id'] = asset_cat

            txt = line.name or ''
            if line.recurring_next_date and (line.recurring_rule_type or '') != 'none':
                if not context:
                    context = {}
                if 'lang' not in context:
                    context['lang'] = self.pool.get('res.users').browse(cr,uid,uid).lang
                start_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                end_date = start_date
                if line.recurring_rule_type == 'dayly':
                    end_date = start_date + relativedelta(days=line.recurring_interval)
                elif line.recurring_rule_type == 'weekly':
                    end_date = start_date + relativedelta(days=line.recurring_interval*7)
                elif line.recurring_rule_type == 'monthly':
                    end_date = start_date + relativedelta(months=line.recurring_interval)
                elif line.recurring_rule_type == 'yearly':
                    end_date = start_date + relativedelta(years=line.recurring_interval)
                if line.recurring_interval > 0:
                    end_date -= relativedelta(days=1)
                if txt:
                    txt += ' - '
                else:
                    txt = ''
                txt += start_date.strftime(date_format) + ' ' + _('to') + ' ' + end_date.strftime(date_format)

            values.update({
                'name': txt,
                'subscription_id': contract.id,
                'subscr_line_id': line.id
            })
            invoice_lines.append((0, 0, values))

        return invoice_lines

    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        values = super(SaleSubscription, self)._prepare_invoice_data(cr, uid, contract, context=context)

        values.update({
            'subscription_id': contract.id,
            'date_invoice': contract.date_start,
        })

        return values

    def _prepare_invoice(self, cr, uid, contract, context={}):
        values = self._prepare_invoice_data(cr, uid, contract, context=context)
        values['invoice_line_ids'] = self._prepare_invoice_lines(cr, uid, contract, values.get('fiscal_position_id', False), context=context)
        return values

    def _prepare_sale_data(self, cr, uid, contract, context=None):
        context = context or {}

        fpos_obj = self.pool['account.fiscal.position']
        partner = contract.partner_id

        if not partner:
            raise UserError(_("You must first select a Customer for Subscription %s!") % contract.name)

        fpos_id = fpos_obj.get_fiscal_position(cr, uid, partner.id, context=context)

        partner_payment_term = partner.property_payment_term_id and partner.property_payment_term_id.id or False

        currency_id = False
        if contract.pricelist_id:
            currency_id = contract.pricelist_id.currency_id.id
        elif partner.property_product_pricelist:
            currency_id = partner.property_product_pricelist.currency_id.id
        elif contract.company_id:
            currency_id = contract.company_id.currency_id.id

        sale = {
            'origin': contract.display_name,
            'partner_id': partner.id,
            'currency_id': currency_id,
            'date_order': contract.date_start,
            'fiscal_position_id': fpos_id,
            'payment_term_id': partner_payment_term,
            'company_id': contract.company_id.id or False,
            'subscription_id': contract.id,
            'project_id': contract.analytic_account_id.id,
        }
        if contract.recurring_next_date:
            next_date = datetime.strptime(contract.recurring_next_date, "%Y-%m-%d")
            periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
            saling_period = relativedelta(**{periods[contract.recurring_rule_type]: contract.recurring_interval})
            new_date = next_date + saling_period
            sale['note'] = _("This sale covers the following period: %s - %s") % (next_date.date(), new_date.date())

        return sale

    def _prepare_sale_line(self, cr, uid, contract, line, fiscal_position, context=None):

        res = line.product_id
        lang_dict = self.get_lang_dict(cr, uid, context=context)
        date_format = lang_dict['date_format']

        values = {
            'name': line.name,
            'sequence': line.sequence,
            'price_unit': line.is_billable and line.price_unit or 0.0,
            'discount': line.discount,
            'product_uom_qty': line.quantity,
            'product_uom': line.uom_id.id or False,
            'product_id': line.product_id.id or False,
            'subscription_id': contract.id,
            'subscr_line_id': line.id,
        }
        if line.requested_date:
            values['requested_date'] = line.requested_date

        txt = line.name or ''
        if line.recurring_next_date and (line.recurring_rule_type or '') != 'none':
            if not context:
                context = {}
            if 'lang' not in context:
                context['lang'] = self.pool.get('res.users').browse(cr,uid,uid).lang
            start_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
            end_date = start_date
            if line.recurring_rule_type == 'dayly':
                end_date = start_date + relativedelta(days=line.recurring_interval)
            elif line.recurring_rule_type == 'weekly':
                end_date = start_date + relativedelta(days=line.recurring_interval*7)
            elif line.recurring_rule_type == 'monthly':
                end_date = start_date + relativedelta(months=line.recurring_interval)
            elif line.recurring_rule_type == 'yearly':
                end_date = start_date + relativedelta(years=line.recurring_interval)
            if line.recurring_interval > 0:
                end_date -= relativedelta(days=1)
            if txt:
                txt += ' - '
            else:
                txt = ''
            txt += start_date.strftime(date_format) + ' ' + _('to') + ' ' + end_date.strftime(date_format)
        values['name'] = txt

        return values

    def _prepare_sale_lines(self, cr, uid, contract, fiscal_position_id, context={}):
        sale_lines = []
        fpos_obj = self.pool.get('account.fiscal.position')
        fiscal_position = None
        if fiscal_position_id:
            fiscal_position = fpos_obj.browse(cr, uid, fiscal_position_id, context=context)

        s_current_date = fields.date.context_today(self, cr, uid)

        for line in contract.recurring_invoice_line_ids:
            if (line.recurring_rule_type or '') != 'none':
                if not line.recurring_next_date or not line.is_active:
                    continue
                line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d') - \
                    relativedelta(days=(line.cancellation_deadline))
                s_line_date = line_date.strftime('%Y-%m-%d')
                if s_current_date < s_line_date:
                    continue
            else:
                if not line.is_active:
                    continue
                if line.recurring_next_date:
                    line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                    s_line_date = line_date.strftime('%Y-%m-%d')
                    if s_current_date != s_line_date:
                        continue

            values = self._prepare_sale_line(cr, uid, contract, line, fiscal_position, context=context)
            sale_lines.append((0, 0, values))

        return sale_lines

    def _prepare_sale(self, cr, uid, contract, context={}):
        sale = self._prepare_sale_data(cr, uid, contract)
        sale['sale_line_ids'] = self._prepare_sale_lines(cr, uid, contract, sale.get('fiscal_position_id', False), context=context)
        return sale

    def setup_sale_filter(self, cr, uid, contract, filter, context={}):
        # Hook to use when looking to an available sale to be completed
        return filter

    def setup_invoice_filter(self, cr, uid, contract, filter, context={}):
        # Hook to use when looking to an available sale to be completed
        return filter

    def _recurring_create_invoice(self, cr, uid, ids, automatic=False, context={}):
        context = context or {}
        invoice_ids = []
        current_date = datetime.now()
        s_current_date = current_date.strftime('%Y-%m-%d')
        if len(ids):
            contracts = ids
        else:
            domain = [
                '|',
                ('recurring_invoice_line_ids.recurring_next_date', '<=', s_current_date),
                ('recurring_invoice_line_ids.is_active', '=', True),
                ('recurring_invoice_line_ids.is_billable', '=', True),
                ('state', 'in', ['open', 'pending']),
                ('type', '=', 'contract')
            ]
            contracts = self.search(cr, uid, domain, context=context)
        if not contracts:
            return invoice_ids

        query = """SELECT a.company_id, array_agg(sub.id) as ids
FROM sale_subscription as sub
JOIN account_analytic_account as a ON
    sub.analytic_account_id = a.id
WHERE sub.id IN %s GROUP BY a.company_id"""
        cr.execute(query, (tuple(contracts),))
        for company_id, ids in cr.fetchall():
            ctx = (context or {}).copy()
            ctx.update({
                'company_id': company_id,
                'force_company': company_id
            })
            for contract in self.browse(cr, uid, ids, context=ctx):

                try:
                    # Prepare the invoice. Its lines list will be empty if there's nothing yet to invoice

                    salesman = contract.manager_id and contract.manager_id.id or uid
                    if not salesman:
                        salesman = uid

                    if contract.recurring_generates == 'sale':
                        sale_values = self._prepare_sale(cr, uid, contract, context=context)
                        if not sale_values.get('sale_line_ids', []):
                            # Nothing to sale, skip this one
                            continue
                        sale_lines = sale_values['sale_line_ids']
                        sale_values['sale_line_ids'] = []

                        # Before creating a new sale, let's see if this partner still has one that is available
                        lst = False
                        if not self.pool.get('ir.values').get_default(cr, uid, 'sale.config.settings', 'auto_done_setting'):
                            # Main setting: sale in 'sale' state may be modified
                            domain = self.setup_sale_filter(cr, uid, contract, [
                                    ('partner_id', '=', contract.partner_id.id),
                                    ('state', '=', 'sale')
                                ], context=context)
                            lst = self.pool('sale.order').search(cr, uid, domain, context=context)
                        if not lst:
                            domain = self.setup_sale_filter(cr, uid, contract, [
                                    ('partner_id', '=', contract.partner_id.id),
                                    ('state', '=', 'draft')
                                ], context=context)
                            
                            lst = self.pool('sale.order').search(cr, uid, domain, context=context)
                        if lst:
                            sale_id = lst[0]
                        else:
                            sale_id = self.pool('sale.order').create(cr, salesman, sale_values, context=context)
                        sale = self.pool('sale.order').browse(cr, uid, sale_id, context=context)
                        for val_item in sale_lines:
                            val = val_item[2]
                            subscr_line = self.pool.get('sale.subscription.line').browse(cr, uid, val['subscr_line_id'], context=context)
                            val['order_id'] = sale_id
                            sale_line_id = self.pool('sale.order.line').create(cr, salesman, val, context=context)
                            self.pool('sale.order.line')._compute_tax_id(cr, uid, [sale_line_id], context=context)
                            if subscr_line.recurring_rule_type == 'none':
                                subscr_line.write({'recurring_next_date': s_current_date, 'is_active': False})

                        invoice_ids.append(sale_id)

                        # Update the recurring next date of each concerned line
                        for line in contract.recurring_invoice_line_ids:
                            if not line.is_active or \
                                not line.recurring_next_date or \
                                line.recurring_rule_type == 'none':
                                continue
                            next_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                            cancel_date = next_date - relativedelta(days=(line.cancellation_deadline or 0))
                            if cancel_date.strftime('%Y-%m-%d') > s_current_date:
                                continue

                            # Compute the recurring next date
                            interval = line.recurring_interval
                            if line.recurring_rule_type == 'daily':
                                next_date += relativedelta(days=+interval)
                            elif line.recurring_rule_type == 'weekly':
                                next_date += relativedelta(weeks=+interval)
                            elif line.recurring_rule_type == 'monthly':
                                next_date += relativedelta(months=+interval)
                            else:
                                next_date += relativedelta(years=+interval)

                        # Load the line with the salesman's context
                            self.pool.get('sale.subscription.line').write(cr, salesman, line.id, {'recurring_next_date': next_date.strftime('%Y-%m-%d')}, context=context)
                            if automatic:
                                cr.commit()
                    else:
                        invoice_values = self._prepare_invoice(cr, uid, contract, context=context)
                        if not invoice_values.get('invoice_line_ids', []):
                            # Nothing to invoice, skip this one
                            continue
                        invoice_lines = invoice_values['invoice_line_ids']
                        invoice_values['invoice_line_ids'] = []

                        # Before creating a new invoice, let's see if this partner still has one in draft mode
                        domain = self.setup_invoice_filter(cr, uid, contract, [
                                ('type', '=', 'out_invoice'),
                                ('partner_id', '=', contract.partner_id.id),
                                ('state', '=', 'draft')
                            ], context=context)
                        lst = self.pool('account.invoice').search(cr, uid, domain, context=context)
                        if lst:
                            invoice_id = lst[0]
                        else:
                            invoice_id = self.pool('account.invoice').create(cr, salesman, invoice_values, context=context)
                        invoice = self.pool('account.invoice').browse(cr, uid,  invoice_id, context=context)
                        for val_item in  invoice_lines:
                            val = val_item[2]
                            subscr_line = self.pool.get('sale.subscription.line').browse(cr, uid, val['subscr_line_id'], context=context)
                            val['invoice_id'] = invoice_id
                            self.pool('account.invoice.line').create(cr, salesman, val, context=context)
                            if subscr_line.recurring_rule_type == 'none':
                                subscr_line.write({'recurring_next_date': s_current_date, 'is_active': False})
                        self.pool['account.invoice'].compute_taxes(cr, salesman, invoice_id, context=context)

                        invoice_ids.append(invoice_id)

                        # Update the recurring next date of each concerned line
                        for line in contract.recurring_invoice_line_ids:
                            if not line.is_active or \
                                not line.recurring_next_date or \
                                line.recurring_rule_type == 'none':
                                continue
                            next_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                            cancel_date = next_date - relativedelta(days=(line.cancellation_deadline or 0))
                            if cancel_date.strftime('%Y-%m-%d') > s_current_date:
                                continue

                            # Compute the recurring next date
                            interval = line.recurring_interval
                            if line.recurring_rule_type == 'daily':
                                next_date += relativedelta(days=+interval)
                            elif line.recurring_rule_type == 'weekly':
                                next_date += relativedelta(weeks=+interval)
                            elif line.recurring_rule_type == 'monthly':
                                next_date += relativedelta(months=+interval)
                            else:
                                next_date += relativedelta(years=+interval)

                        # Load the line with the salesman's context
                            self.pool.get('sale.subscription.line').write(cr, salesman, line.id, {'recurring_next_date': next_date.strftime('%Y-%m-%d')}, context=context)
                            if automatic:
                                cr.commit()
                except Exception:
                    if automatic:
                        cr.rollback()
                        _logger.exception('Fail to create recurring invoice for contract %s', contract.code)
                    else:
                        raise
        return invoice_ids

    # ---------- Scheduler

    def _cron_recurring_create_invoice(self, cr, uid, context=None):
        return self._recurring_create_invoice(cr, uid, [], automatic=True, context=context)


class SaleSubscriptionLine(osv.osv):
    _inherit = 'sale.subscription.line'

    # ---------- Fields management

    _columns = {
        'recurring_rule_type': fields.selection([
                ('none', 'None'),
                ('daily', 'Day(s)'),
                ('weekly', 'Week(s)'),
                ('monthly', 'Month(s)'),
                ('yearly', 'Year(s)')
            ],
            'Recurrency',
            required=True,
            help="Invoice automatically repeat at specified interval"),
        'recurring_interval': fields.integer('Interval', help="Repeat every (Days/Week/Month/Year)"),
        'recurring_next_date': fields.date('Next Action'),

        'is_active': fields.boolean(string='Active'),
        'is_billable': fields.boolean(string='Billable'),
        'sequence': fields.integer(string='Sequence'),
        'cancellation_deadline': fields.integer(string='Days before'),
        'requested_date': fields.date(string='Requested Date')
    }
    _defaults = {
        'recurring_rule_type': lambda *a: 'none',
        'recurring_interval': lambda *a: 1,
        'is_active': lambda *a: True,
        'is_billable': lambda *a: True,
        'sequence': lambda *a: 1,
        'cancellation_deadline': lambda *a: 0
    }

    # ---------- Utils

    def _compute_tax_id(self, cr, uid, ids, context={}):
        return super(SaleSubscriptionLine, self)._compute_tax_id(cr, uid, ids, context=context)

    # ---------- UI management

    def product_id_change(
            self, cr, uid, ids,
            product, uom_id, qty=0, name='', partner_id=False,
            price_unit=False, pricelist_id=False, company_id=None,
            context={}
        ):

        res = super(SaleSubscriptionLine, self).product_id_change(
            cr, uid, ids,
            product, uom_id, qty=qty, name=name, partner_id=partner_id,
            price_unit=price_unit, pricelist_id=pricelist_id, company_id=company_id,
            context=context
        )

        if product:
            if 'value' not in res:
                res['value'] = {}
            ProductProduct = self.pool.get('product.product')
            ctx = (context or {}).copy()
            ctx.update({
                'company_id': company_id,
                'force_company': company_id,
                'pricelist': pricelist_id
            })
            prod = ProductProduct.browse(cr, uid, product, context=ctx)
            if prod.recurring_rule_type and prod.recurring_interval:
                next_date = datetime.now()
                failed = True
                if prod.recurring_rule_type == 'daily':
                    next_date += relativedelta(days=prod.recurring_interval or 1)
                    failed = False
                elif prod.recurring_rule_type == 'weekly':
                    next_date += relativedelta(days=7*(prod.recurring_interval or 1))
                    failed = False
                elif prod.recurring_rule_type == 'monthly':
                    next_date += relativedelta(months=prod.recurring_interval or 1)
                    failed = False
                elif prod.recurring_rule_type == 'yearly':
                    next_date += relativedelta(years=prod.recurring_interval or 1)
                    failed = False
                if failed:
                    res['value'].update({
                        'recurring_rule_type': 'none',
                        'recurring_interval': 1,
                        'recurring_next_date': None
                    })
                else:
                    res['value'].update({
                        'recurring_rule_type': prod.recurring_rule_type,
                        'recurring_interval': prod.recurring_interval,
                        'recurring_next_date': next_date
                    })

        return res
