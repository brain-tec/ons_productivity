# -*- coding: utf-8 -*-
#
#  File: models/procurements.py
#  Module: ons_productivity_procurement_adv
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2018-TODAY Open-Net Ltd. All rights reserved.
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    @api.model
    def run(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        values.setdefault('company_id', self.env['res.company']._company_default_get('procurement.group'))
        values.setdefault('priority', '1')
        values.setdefault('date_planned', fields.Datetime.now())
        rule = self._get_rule(product_id, location_id, values)

        if not rule:
            msg = _("No procurement rule found for the product '%s' (ID=%d) at the location '%s'. " +\
                    "Please verify the configuration of your routes") % \
                  (product_id.name, product_id.id, location_id.complete_name)

            raise UserError(msg)

        return super(ProcurementGroup, self).run(product_id, product_qty, product_uom, location_id, name, origin, values)

