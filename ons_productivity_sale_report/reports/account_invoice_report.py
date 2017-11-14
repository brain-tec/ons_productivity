# -*- coding: utf-8 -*-
#
#  File: reports/account_invoice_report.py
#  Module: ons_productivity_base
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open-Net Sàrl All rights reserved.

from odoo import tools
from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    @api.model_cr
    def init(self):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM (
                %s %s %s
            ) AS sub
            LEFT JOIN res_currency_rate cr ON
                (cr.currency_id = sub.currency_id AND
                 cr.company_id = sub.company_id AND
                 cr.name <= COALESCE(sub.date, NOW()) AND
                 (cr.date_to IS NULL OR cr.date_to > COALESCE(sub.date, NOW())))
        )""" % (
                    self._table, self._select(), self._sub_select(), self._from(), self._group_by()))
