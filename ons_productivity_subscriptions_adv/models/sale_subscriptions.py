# -*- coding: utf-8 -*-
#
#  File: models/sale_subscriptions.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#  MIG[10.0] by lfr@open-net.ch (2017)
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. All rights reserved.
##############################################################################


from odoo import models, fields, api
import odoo.tools as tools
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    # ---------- Fields management
    @api.multi
    @api.depends('recurring_invoice_line_ids.recurring_next_date')
    def _comp_next_date(self):
        _logger.info("COMPUTE: _comp_next_date")
        for contract in self:
            min_date = False
            for line in contract.recurring_invoice_line_ids:
                if not line.is_active or \
                    not line.is_billable or \
                    line.recurring_rule_type == 'none' or \
                    not line.recurring_rule_type or \
                    not line.recurring_next_date:
                    continue
                before = line.recurring_next_date
                if not min_date:
                    min_date = before
                    continue
                if before > min_date:
                    continue
                min_date = before
            contract.recurring_next_date = min_date
            _logger.info("-CONT_MIN-DATE-: %s" % contract.recurring_next_date)

    @api.multi
    def _get_sales_count(self):
        _logger.info("GET: _get_sales_count")
        SaleSubscription = self.env['sale.order']
        for subscr in self:
            subscr.sales_count = len(SaleSubscription.search([('subscription_id','=',subscr.id)]))

    @api.multi
    def _get_invoices_count(self):
        _logger.info("GET: _get_invoices_count")
        InvoiceSubscription = self.env['account.invoice']
        for subscr in self:
            subscr.invoices_count = len(InvoiceSubscription.search([('subscription_id','=',subscr.id)]))

    @api.multi
    @api.depends('line_ids', 'recurring_invoice_line_ids')
    def _get_non_recurring_price(self):
        _logger.info("GET: _get_non_recurring_price")
        for account in self:
            for line in account.recurring_invoice_line_ids:
                if line.is_active and (not line.recurring_rule_type or line.recurring_rule_type == 'none'):
                    account.non_recurring_total =+ line.price_subtotal

    @api.multi
    @api.depends('line_ids', 'recurring_invoice_line_ids')
    def _get_recurring_price(self):
        _logger.info("GET: _get_recurring_price")
        for account in self:
            for line in account.recurring_invoice_line_ids:
                if line.is_active and line.recurring_rule_type and line.recurring_rule_type != 'none':
                    account.recurring_total =+ line.price_subtotal


    recurring_rule_type = fields.Selection([
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)')
        ],
        'Recurrency',
        help="Invoice automatically repeat at specified interval",
        readonly=True,
        default=lambda *a: 'daily')

    recurring_interval = fields.Integer(
        'Repeat Every', 
        help="Repeat every (Days/Week/Month/Year)", 
        readonly=True,
        default=lambda *a: 1)

    recurring_next_date = fields.Date(
        string='Date of Next Invoice',
        store=True,
        compute=_comp_next_date)

    recurring_generates = fields.Selection([
            ('invoice', 'An invoice'),
            ('sale', 'A sale'),
        ],
        'Generates',
        default='invoice')

    sales_count = fields.Integer(
        string='Sales count',
        compute=_get_sales_count)

    invoices_count = fields.Integer(
        string='Invoices count',
        compute=_get_invoices_count)

    non_recurring_total = fields.Float(
        string="Non-recurring Price",
        store=True,
        compute=_get_non_recurring_price)

    recurring_total = fields.Float(
        string="Recurring Price",
        type="float",
        store=True, 
        compute=_get_recurring_price)

    manager_id = fields.Many2one(
        'res.users', 
        'Person in charge')

    asset_category_id = fields.Many2one(
        'account.asset.category', 
        'Deferred Revenue',
        help="This asset category will be applied to the lines of the contract's invoices.",
        domain="[('type','=','sale')]")

    # ---------- Instances management
    @api.model
    def create(self, vals):
        date_start = vals.get('date_start')

        new_id = super(SaleSubscription, self).create(vals)

        if new_id and date_start:
            new_id.update_lines_date_start(date_start)

        return new_id

    @api.multi
    def write(self, vals):
        date_start = vals.get('date_start')

        ret = super(SaleSubscription, self).write(vals)

        if date_start:
            self.update_lines_date_start(date_start)

        return ret

    @api.onchange('template_id')
    def on_change_template(self):
        res = super(SaleSubscription, self).on_change_template()
        for subs in self:
            if subs.template_id:
                if not subs.date_start:
                    subs.date_start = datetime.now()

                ProductProduct = subs.env['product.product']
                ctx = {}
                if subs.pricelist_id:
                    ctx['pricelist'] = subs.pricelist_id

                invoice_line_ids = []
                for x in subs.recurring_invoice_line_ids:

                    line_item = {
                        'product_id': x.product_id.id,
                        'uom_id': x.uom_id.id,
                        'name': x.name,
                        'sold_quantity': x.quantity,
                        'price_unit': x.price_unit or 0.0,
                        'discount': x.discount or 0.0,
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
                        if subs.date_start:
                            next_date = datetime.strptime(subs.date_start, '%Y-%m-%d')
                            line_item.update({
                                'recurring_rule_type': x.recurring_rule_type,
                                'recurring_interval': x.recurring_interval,
                                'recurring_next_date': next_date
                            })
                    invoice_line_ids.append((0, 0, line_item))
                    subs.recurring_invoice_line_ids = invoice_line_ids
                else:
                    return res

    # Show the list of corresponding invoices
    @api.multi
    def action_subscription_invoice(self):
        list_view_id = self.env.ref('account.invoice_tree').id
        form_view_id = self.env.ref('account.invoice_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.invoice",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["subscription_id", "in", [subscription.id for subscription in self]]],
            "context": {"create": False},
            "name": _("Invoices"),
        }

    # Show the list of corresponding sales
    @api.multi
    def action_subscription_sale(self):
        list_view_id = self.env.ref('sale.view_order_tree').id
        form_view_id = self.env.ref('ons_productivity_subscriptions_adv.onsp_view_sale_order_subscription_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["subscription_id", "in", [subscription.id for subscription in self]]],
            "context": {"create": False},
            "name": _("Sales"),
        }

    # Generate an invoice/a sale
    @api.multi
    def action_recurring_invoice(self):
        return self.recurring_invoice()

    # ---------- Utils
    @api.multi
    def update_lines_date_start(self, new_date_start):
        SaleSubscriptionLines = self.env['sale.subscription.line']
        for subscription in self:
            lines = subscription.recurring_invoice_line_ids.search([('recurring_rule_type','!=','none')])
            if len(lines):
                lines.write({'recurring_next_date': new_date_start})

        return True

    @api.multi
    def get_lang_dict(self):
        pool_lang = self.env['res.lang']
        lang = self._context.get('lang', 'en_US') or 'en_US'
        lang_obj = pool_lang.search([('code','=',lang)])[0]

        return {'lang_obj':lang_obj,'date_format':lang_obj.date_format,'time_format':lang_obj.time_format}

    @api.multi
    def recurring_invoice(self):
        return self._recurring_create_invoice()

    @api.multi
    def _prepare_invoice_line(self, line, fiscal_position):
        values = super(SaleSubscription, self)._prepare_invoice_line(line, fiscal_position)
        if not line.is_billable:
            values['price_unit'] = 0
        _logger.info("INFO_prep_invoice_line: %s" % values)
        return values

    @api.multi
    def _prepare_invoice_lines(self, fiscal_position_id):
        invoice_lines = []
        fpos_obj = self.env['account.fiscal.position']
        fiscal_position = fpos_obj.browse(fiscal_position_id)
        _logger.info("HERE+FISCAL: %s" % fiscal_position)
        lang_dict = self.get_lang_dict()
        date_format = lang_dict['date_format']

        current_date = datetime.now()
        s_current_date = current_date.strftime('%Y-%m-%d')
        for contract in self:
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

                values = contract._prepare_invoice_line(line, fiscal_position)
                if line.use_new_so_inv:
                    values['use_new_so_inv'] = True

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
                        asset_cat = self.env['account.asset.category'].browse(asset_cat[0])
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
            _logger.info("INFO_prep_invoice_lines: %s" % invoice_lines)
        return invoice_lines

    @api.multi
    def _prepare_invoice_data(self):
        values = super(SaleSubscription, self)._prepare_invoice_data()
        for subs in self: 
            values.update({
                'comment': '',
                'subscription_id': subs.id,
                'date_invoice': datetime.now().strftime('%Y-%m-%d'),
            })
        return values

    @api.multi
    def _prepare_invoice(self):
        for contract in self:
            if not contract.recurring_next_date:
                contract.recurring_next_date = datetime.now().strftime('%Y-%m-%d')
            values = contract._prepare_invoice_data()
            values['invoice_line_ids'] = contract._prepare_invoice_lines(values.get('fiscal_position_id', False))
        return values

    @api.multi
    def _prepare_sale_data(self):
        for contract in self:
            fpos_obj = self.env['account.fiscal.position']
            partner = contract.partner_id

            if not partner:
                raise UserError(_("You must first select a Customer for Subscription %s!") % contract.name)

            fpos_id = fpos_obj.get_fiscal_position(partner.id)

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
                'date_order': datetime.now().strftime('%Y-%m-%d'),
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

    @api.multi
    def _prepare_sale_line(self, line, fiscal_position_id):
        for subs in self:
            res = line.product_id
            lang_dict = subs.get_lang_dict()
            date_format = lang_dict['date_format']

            values = {
                'name': line.name,
                'sequence': line.sequence,
                'price_unit': line.is_billable and line.price_unit or 0.0,
                'discount': line.discount,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id or False,
                'product_id': line.product_id.id or False,
                'subscription_id': subs.id,
                'subscr_line_id': line.id,
            }
            if line.requested_date:
                values['requested_date'] = line.requested_date
            if line.use_new_so_inv:
                values['use_new_so_inv'] = True

            txt = line.name or ''
            if line.recurring_next_date and (line.recurring_rule_type or '') != 'none':
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

    @api.multi
    def _prepare_sale_lines(self, fiscal_position_id):
        for prep in self:
            sale_lines = []
            fpos_obj = prep.env['account.fiscal.position']
            fiscal_position = fpos_obj.browse(fiscal_position_id)
            _logger.info("ENTERED")
            current_date = datetime.now()
            s_current_date = current_date.strftime('%Y-%m-%d')
            for line in prep.recurring_invoice_line_ids:
                if (line.recurring_rule_type or '') != 'none':
                    if not line.recurring_next_date or not line.is_active:
                        continue
                    _logger.info("E+1")
                    line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d') - \
                        relativedelta(days=(line.cancellation_deadline))
                    s_line_date = line_date.strftime('%Y-%m-%d')
                    if s_current_date < s_line_date:
                        continue
                    _logger.info("E+1.1")
                else:
                    if not line.is_active:
                        continue
                    _logger.info("E+2")
                    if line.recurring_next_date:
                        line_date = datetime.strptime(line.recurring_next_date, '%Y-%m-%d')
                        s_line_date = line_date.strftime('%Y-%m-%d')
                        if s_current_date != s_line_date:
                            continue
                    _logger.info("E+2.2")

                values = prep._prepare_sale_line(line, fiscal_position)
                sale_lines.append((0, 0, values))

        return sale_lines

    @api.multi
    def _prepare_sale(self):
        for contract in self:
            if not contract.recurring_next_date:
                contract.recurring_next_date = datetime.now().strftime('%Y-%m-%d')
            sale = contract._prepare_sale_data()
            sale['sale_line_ids'] = contract._prepare_sale_lines(sale.get('fiscal_position_id', False))
        return sale

    @api.multi
    def setup_sale_filter(self, contract, filter):
        # Hook to use when looking to an available sale to be completed
        return filter

    @api.multi
    def setup_invoice_filter(self, contract, filter):
        # Hook to use when looking to an available invoice to be completed
        return filter


    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        AccountInvoice = self.env['account.invoice']
        SaleOrder = self.env['sale.order']
        invoices = []
        s_current_date = datetime.now()
        current_date = s_current_date.strftime('%Y-%m-%d')
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        cust_domain = [
            '|',
            ('recurring_invoice_line_ids.recurring_next_date', '<=', current_date),
            ('recurring_invoice_line_ids.is_active', '=', True),
            ('recurring_invoice_line_ids.is_billable', '=', True),
            ('state', 'in', ['open', 'pending']),
            ('type', '=', 'contract')
        ]
        domain = [('id', 'in', self.ids)] if self.ids else cust_domain
        sub_data = self.search_read(fields=['id', 'company_id'], domain=domain)
        try:
            _logger.info("INFO_:: %s" % set(data['company_id'][0] for data in sub_data))
            for company_id in set(data['company_id'][0] for data in sub_data):
                sub_ids = map(lambda s: s['id'], filter(lambda s: s['company_id'][0] == company_id, sub_data))
                subs = self.with_context(company_id=company_id, force_company=company_id).browse(sub_ids)

                ctx = dict(company_id = company_id, force_company = company_id)

                salesman = self.manager_id and self.manager_id.id or self.env.uid
                if not salesman:
                    salesman = self.env.uid
                for sub in subs:
                    if sub.recurring_generates == 'sale':
                        _logger.info("---SALE---")
                        sale_values = sub._prepare_sale()
                        if not sale_values.get('sale_line_ids', []):
                            # Nothing to sale, skip this one
                            continue
                        sale_lines = sale_values['sale_line_ids']
                        sale_values['sale_line_ids'] = []

                        # Before creating a new sale, let's see if this partner still has one that is available
                        lst = False

                        if not self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
                            # Main setting: sale in 'sale' state may be modified
                            domain_sale = self.setup_sale_filter(sub, [
                                    ('partner_id', '=', sub.partner_id.id),
                                    ('state', '=', 'sale')
                                ])
                        else:
                            domain_sale = self.setup_sale_filter(sub, [
                                    ('partner_id', '=', sub.partner_id.id),
                                    ('state', '=', 'draft')
                                ])
                        lst = SaleOrder.with_context(ctx).search(domain_sale)

                        
                        # A contract line may request a new sale
                        for line in sale_lines:
                            if line[2].get('use_new_so_inv'):
                                lst = False
                                del line[2]['use_new_so_inv']

                        if lst:
                            sale_id = lst[0]
                        else:
                            sale_values['user_id'] = salesman
                            sale_id = SaleOrder.with_context(ctx).create(sale_values)

                        sale = SaleOrder.with_context(ctx).browse(sale_id)
                        for val_item in sale_lines:
                            val = val_item[2]
                            subscr_line = self.env['sale.subscription.line'].with_context(ctx).browse(val['subscr_line_id'])
                            val['order_id'] = sale_id.id
                            sale_line_id = self.env['sale.order.line'].with_context(ctx).create(val)
                            if subscr_line.recurring_rule_type == 'none':
                                subscr_line.write({'recurring_next_date': current_date, 'is_active': False})
                        sale_line_id.with_context(ctx)._compute_tax_id()
                        invoices.append(sale_id)
                    else:
                        _logger.info("---INVOICE---")
                        invoice_values = sub._prepare_invoice()
                        if not invoice_values.get('invoice_line_ids', []):
                            # Nothing to invoice, skip this one
                            continue
                        invoice_lines = invoice_values['invoice_line_ids']
                        invoice_values['invoice_line_ids'] = []

                        # Before creating a new invoice, let's see if this partner still has one in draft mode
                        domain_invoice = self.setup_invoice_filter(sub, [
                                ('type', '=', 'out_invoice'),
                                ('partner_id', '=', sub.partner_id.id),
                                ('state', '=', 'draft')
                            ])
                        lst = AccountInvoice.with_context(ctx).search(domain_invoice)

                        # A contract line may request a new sale
                        for line in invoice_lines:
                            if line[2].get('use_new_so_inv'):
                                lst = False
                                del line[2]['use_new_so_inv']

                        if lst:
                            invoice_id = lst[0]
                        else:
                            invoice_values['user_id'] = salesman
                            invoice_id = AccountInvoice.with_context(ctx).create(invoice_values)

                        invoice = AccountInvoice.with_context(ctx).browse(invoice_id)

                        for val_item in invoice_lines:
                            val = val_item[2]
                            subscr_line = self.env['sale.subscription.line'].with_context(ctx).browse(val['subscr_line_id'])
                            val['invoice_id'] = invoice_id.id
                            val['user_id'] = salesman
                            self.env['account.invoice.line'].with_context(ctx).create(val)
                            if subscr_line.recurring_rule_type == 'none':
                                subscr_line.write({'recurring_next_date': current_date, 'is_active': False})
                        invoice_id['user_id'] = salesman
                        invoice_id.with_context(ctx).compute_taxes()

                        invoices.append(invoice_id)

                    invoices[-1].message_post_with_view('mail.message_origin_link',
                     values={'self': invoices[-1], 'origin': sub},
                     subtype_id=self.env.ref('mail.mt_note').id)

                    for line in sub.recurring_invoice_line_ids:
                        if not line.is_active or \
                            not line.recurring_next_date or \
                            line.recurring_rule_type == 'none':
                            continue

                        next_date = fields.Date.from_string(line.recurring_next_date or current_date)
                        cancel_date = next_date - relativedelta(days=(line.cancellation_deadline or 0))
                        if cancel_date.strftime('%Y-%m-%d') > current_date:
                            continue

                        rule, interval = line.recurring_rule_type, line.recurring_interval
                        new_date = next_date + relativedelta(**{periods[rule]: interval})
                        line.recurring_next_date = new_date
                    _logger.info(": %s : DONE" % sub.recurring_generates)
                    if automatic:
                        self.env.cr.commit()

        except Exception:
            if automatic:
                self.env.cr.rollback()
                _logger.exception('Fail to create recurring invoice for subscription %s', sub.code)
            else:
                raise
        return invoices

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    # ---------- Fields management

    recurring_rule_type = fields.Selection([
            ('none', 'None'),
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)')
        ],
        'Recurrency',
        required=True,
        help="Invoice automatically repeat at specified interval",
        default=lambda *a: 'none')

    recurring_interval = fields.Integer(
        'Interval', 
        help="Repeat every (Days/Week/Month/Year)",
        default=lambda *a: 1)

    recurring_next_date = fields.Date(
        'Next Action')

    is_active = fields.Boolean(
        string='Active',
        default=lambda *a: True)

    is_billable = fields.Boolean(
        string='Billable',
        default=lambda *a: True)

    sequence = fields.Integer(
        string='Sequence',
        default=lambda *a: 1)

    cancellation_deadline = fields.Integer(
        string='Days before',
        default=lambda *a: 0)

    requested_date = fields.Date(
        string='Requested Date')

    use_new_so_inv = fields.Boolean(
        string='New sale/invoice',
        default=lambda *a: False)

    sale_layout_cat_id = fields.Many2one(
        'sale.layout_category',
        string='Sale Layout Category')

    # ---------- Utils
    @api.multi
    def _compute_tax_id(self):
        return super(SaleSubscriptionLine, self)._compute_tax_id()
