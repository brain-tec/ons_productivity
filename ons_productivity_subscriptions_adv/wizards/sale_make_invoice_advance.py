#
#  File: wizards/sale_make_invoice_advance.py
#  Module: ons_productivity_subscriptions_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>


from odoo import api, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if not invoice or not order:
            return invoice

        for line in invoice.invoice_line_ids:
            line.subscription_id = so_line.subscription_id
            line.subscr_line_id = so_line.subscr_line_id

            # Overwrite sale_contract_asset's default asset handling:
            #   the info is now computed from the line's recurrence
            #   it defaults from the product if empty
            asset_cat = False
            if so_line.subscr_line_id:
                month = 0
                if so_line.subscr_line_id.recurring_rule_type in ('dayly','weekly'):
                    month = 1
                elif so_line.subscr_line_id.recurring_rule_type == 'monthly':
                    month = so_line.subscr_line_id.recurring_interval
                elif so_line.subscr_line_id.recurring_rule_type == 'yearly':
                    month = so_line.subscr_line_id.recurring_interval * 12
                if month:
                    asset_cat = self.env['account.asset.category'].search([('active','=',True),('method_number','=',month)])
                    if asset_cat:
                        asset_cat = asset_cat[0].id
                    else:
                        asset_cat = False
                if not asset_cat and line.product_id.product_tmpl_id.deferred_revenue_category_id:
                    asset_cat = line.product_id.product_tmpl_id.deferred_revenue_category_id.id or False

            line.asset_category_id = asset_cat

        return invoice

    @api.multi
    def create_invoices(self):
        return super(SaleAdvancePaymentInv, self).create_invoices()
