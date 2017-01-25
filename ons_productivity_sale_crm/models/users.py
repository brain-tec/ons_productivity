# -*- coding: utf-8 -*-
#
# File: model/users.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models
from datetime import date


class ResUsers(models.Model):
    _inherit = 'res.users'

    yearly_planned_invoiced_amount = fields.Monetary(string='Yearly planned')
