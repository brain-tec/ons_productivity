# -*- coding: utf-8 -*-
#
#  File: models/product.py
#  Module: ons_productivity_mrp
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _
from openerp.osv import fields

import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'

    def compute_price(self, cr, uid, product_ids, template_ids=False, recursive=False, test=False, real_time_accounting = False, context=None):
        '''
        Will return test dict when the test = False
        Multiple ids at once?
        testdict is used to inform the user about the changes to be made
        '''
        return super(product_template, self).compute_price(cr, uid, product_ids, template_ids=template_ids, recursive=recursive, test=test, real_time_accounting = real_time_accounting, context=context)

    def _calc_price(self, cr, uid, bom, test = False, real_time_accounting=False, context=None):
        if context is None:
            context={}
        price = 0
        uom_obj = self.pool.get("product.uom")
        tmpl_obj = self.pool.get('product.template')
        for sbom in bom.bom_line_ids:
            my_qty = sbom.product_qty
            if not sbom.attribute_value_ids:
                # No attribute_value_ids means the bom line is not variant specific
                price += uom_obj._compute_price(cr, uid, sbom.product_id.uom_id.id, sbom.product_id.standard_price, sbom.product_uom.id) * my_qty

        if bom.routing_id:
            for wline in bom.routing_id.workcenter_lines:
                wc = wline.workcenter_id
                coeff = 1.0
                if wc:
                    for wkc_param in bom.workcenter_param_ids:
                        if not wkc_param.name:
                            continue
                        if wkc_param.name.id == wc.id:
                            coeff = wkc_param.coeff
                            break
                cycle = wline.cycle_nbr
                hour = (wc.time_start + wc.time_stop + cycle * wc.time_cycle) *  (wc.time_efficiency or 1.0)
                price += (wc.costs_cycle * cycle + wc.costs_hour * hour) * coeff
                price = self.pool.get('product.uom')._compute_price(cr,uid,bom.product_uom.id, price, bom.product_id.uom_id.id)
        
        #Convert on product UoM quantities
        if price > 0:
            price = uom_obj._compute_price(cr, uid, bom.product_uom.id, price / bom.product_qty, bom.product_id.uom_id.id)

        product = tmpl_obj.browse(cr, uid, bom.product_tmpl_id.id, context=context)
        if not test:
            if (product.valuation != "real_time" or not real_time_accounting):
                tmpl_obj.write(cr, uid, [product.id], {'standard_price' : price}, context=context)
            else:
                #Call wizard function here
                wizard_obj = self.pool.get("stock.change.standard.price")
                ctx = context.copy()
                ctx.update({'active_id': product.id, 'active_model': 'product.template'})
                wiz_id = wizard_obj.create(cr, uid, {'new_price': price}, context=ctx)
                wizard_obj.change_price(cr, uid, [wiz_id], context=ctx)
        return price
