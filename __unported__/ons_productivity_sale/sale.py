# -*- coding: utf-8 -*-
#
#  File: sale.py
#  Module: ons_productivity_sale
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields,osv
from openerp.tools.translate import _
from openerp.tools import float_compare
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    _columns = {
        'parent_partner_id': fields.many2one('res.partner', 'Parent'),
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        ret = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        ret.update({
            'sale_id': order and order.id or False,
            })
        
        return ret

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        result = super(sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if not partner_id:
            if result.get('value', {}):
                result['value']['parent_partner_id'] = False
            return result
        partner = self.pool.get('res.partner').read(cr, uid, partner_id, ['parent_id'], context=context)
        result['value']['parent_partner_id'] = partner and partner.get('parent_id', False) or False
        
        return result

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        result = super(sale_order,self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            check = self.pool.get('ir.values').get_default(cr, uid, self._name, 'onsp_sale_partner_companies_only')
            _logger.debug(" ****************************** Check companies only="+(check and "true" or "false"))
            if check:
                doc = etree.XML(result['arch'])
                nodes = doc.xpath("//form/sheet/group[1]/group[1]/field[@name='partner_id']")
                for node in nodes:
                    context = eval(node.attrib.get('context', '{}'))
                    if not context.get('default_is_company', False):
                        context['search_default_type_company'] = 1
                    node.set('context', str(context))
                result['arch'] = etree.tostring(doc)
                if result['fields'].get('partner_id', {}):
                    result['fields']['partner_id']['domain'] += [('is_company','!=',False)]
        
        return result

sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):

        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                        uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, 
                        date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        
        if not res.get('value',{}) or not product: return res

        # Retrieve the product
        product_obj = self.pool.get('product.product')
        prod = product_obj.browse(cr, uid, product, context=context)
        
        # Check its availability
        product_uom_obj = self.pool.get('product.uom')
        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if prod.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if not uom2:
            uom2 = prod.uom_id
        
        res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
        compare_qty = float_compare(prod.virtual_available * uom2.factor, qty * prod.uom_id.factor, precision_rounding=prod.uom_id.rounding)
        if (prod.type=='product') and \
            ( (prod.procure_method=='make_to_order') or \
              (int(compare_qty) == -1 and prod.procure_method=='make_to_stock') ):
            delay = 0
            for suppl in prod.seller_ids:
                delay = max(delay, suppl.delay)
            if not res['value'].get('delay', False):
                res['value']['delay'] = 0.0
            res['value']['delay'] += delay
        
        return res

sale_order_line()
