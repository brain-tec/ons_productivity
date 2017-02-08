# -*- encoding: utf-8 -*-
#
#  File: models/sale_team.py
#  Module: ons_productivity_sale_crm
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open-Net Ltd. All rights reserved.
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from datetime import date


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    group_sale_target = fields.Boolean(string="Yearly planned", default=False)
    group_invoiced_planned = fields.Monetary(string="Yearly planned")
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
