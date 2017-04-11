# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'


    page_break = fields.Boolean(
        string="Page Break",
        help="Do a page break after this")

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceLine, self).create(vals)
        if res.sale_line_ids:
            res.page_break = any(res.sale_line_ids.mapped("page_break"))
        return res

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def order_lines_layouted(self):
        res = super(AccountInvoice, self).order_lines_layouted()

        new_layout = [[]]

        for page in res:
            for category in page:
                for line in category['lines']:
                    if line.page_break:
                        new_layout[-1].append(category)
                        new_layout.append([])
                    else:
                        new_layout[-1].append(category)
        return new_layout