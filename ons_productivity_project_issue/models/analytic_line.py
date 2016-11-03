# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'
    _order = 'tag_ids ASC, date ASC'

    ons_to_invoice = fields.Boolean(string="Invoiceable", default=True)