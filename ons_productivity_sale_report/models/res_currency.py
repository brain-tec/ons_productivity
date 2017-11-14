# -*- coding: utf-8 -*-
#
#  File: models/res_currency.py
#  Module: ons_productivity_sale_report
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open-Net Sàrl All rights reserved.


from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    # ---------- Fields management
    
    date_to = fields.Datetime(string='Date to', compute='_comp_date_to', index=True, store=True)

    @api.multi
    @api.depends('name','rate','currency_id','currency_id.rate_ids')
    def _comp_date_to(self):
        use_company = (len(self.env['res.company'].search([])) > 1)

        for rate in self:
            if use_company:
                if rate.company_id:
                    comp_query = " AND (company_id IS NULL OR company_id = %d)" % (rate.company_id,)
                else:
                    comp_query = " AND company_id IS NULL"
            else:
                comp_query = ""

            query = """SELECT name
FROM res_currency_rate
WHERE name > '%s' AND currency_id = %d %s
ORDER BY name LIMIT 1""" % \
                    (str(rate.name), rate.currency_id, comp_query)
            self._cr.execute(query)
            row = self._cr.fetchone()
            rate.date_to = row and row[0] or False

    @api.model
    def create(self, vals):
        new_id = super(CurrencyRate, self).create(vals)

        use_company = (len(self.env['res.company'].search([])) > 1)
        if use_company:
            if rate.company_id:
                comp_query = " AND (company_id IS NULL OR company_id = %d)" % (rate.company_id,)
            else:
                comp_query = " AND company_id IS NULL"
        else:
            comp_query = ""

        query = """UPDATE res_currency_rate
        set date_to='%s'
        WHERE id in (SELECT id FROM res_currency_rate 
              WHERE name < '%s' AND currency_id = %d %s
              ORDER BY name desc LIMIT 1)""" % \
                (new_id.name, new_id.name, new_id.currency_id, comp_query)
        self._cr.execute(query)
