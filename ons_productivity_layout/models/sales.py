# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    page_break = fields.Boolean(
        string="Page Break",
        help="Do a page break after this")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def order_lines_layouted(self):
        res = super(SaleOrder, self).order_lines_layouted()

        new_layout = [[]]
        for page in res:
            for category in page:
                has_page_break = False
                for line in category['lines']:
                    if line.page_break:
                        has_page_break = True
                if has_page_break:
                    new_layout[-1].append(category)
                    new_layout.append([])
                else:
                    new_layout[-1].append(category)
        return new_layout