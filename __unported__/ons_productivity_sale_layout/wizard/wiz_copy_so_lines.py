# -*- encoding: utf-8 -*-
#
#  File: wizard/wiz_copy_so_lines.py
#  Module: ons_productivity_sale_layout
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open-Net Ltd. All rights reserved.
##############################################################################
#
# Author Yvon Philippe Crittin / Open Net Sarl
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
from tools.translate import _
import time

def _get_so_ids(self, cr, uid, context=None):
    ret = []
    if context.get('active_model', '') == 'sale.order' and context.get('active_id', False):
        sol_pool = self.pool.get('sale.order.line')
        ids = sol_pool.search(cr, uid, [('order_id', '=', context['active_id'])], context=context)
        res = sol_pool.read(cr, uid, ids, ['sequence', 'layout_type', 'name'], context)
        ret = [(str(r['id']), u"%d: %s - %s" % (r['sequence'], r['layout_type'], r['name'])) for r in res]
    return ret

class wiz_copy_so_lines(osv.osv_memory):
    _name = 'onsp.wiz_copy_so_lines'
    _description = 'Open-Net wizard: copy/import sale order lines'
    
    # ---------- Fields management

    _columns = {
        'so_id': fields.many2one('sale.order', 'Sale order', required=True),
        'sol_ids': fields.many2many('sale.order.line', 'wiz_copy_so_lines_rel', 'wiz_id', 'sol_id', 'Sale order lines'),
        'lines': fields.selection(_get_so_ids, "Before"),
    }
    
    _defaults = {
        'so_id': lambda s,c,u,ct: ct.get('active_model','') == 'sale.order' and ct.get('active_id', False) or False,
    }

    def do_it(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        datas = self.browse(cr, uid, ids[0], context=context)
        
        sale_obj = self.pool.get('sale.order')
        sols_obj = self.pool.get('sale.order.line')
        
        # Retrieve the current sequence number
        self_so = sale_obj.browse(cr, uid, context.get('active_id', False), context=context)
        if not self_so:
            return {}
        seq = 0
        for line in self_so.order_line:
            if seq < line.sequence:
                seq = line.sequence
        if datas.lines:
            nb = len(datas.sol_ids)
            if nb:
                seq = 0
                found = False
                for line in self_so.order_line:
                    if not found:
                        if line.id == int(datas.lines):
                            found = True
                        else:
                            seq = line.sequence
                            continue

                    line.write({'sequence': line.sequence + nb*10}, context=context)

        # Duplicate the selected lines
        for line in datas.sol_ids:
            seq += 10
            defaults = {
                'order_id': self_so.id,
                'sequence': seq,
                'invoice_lines': [(6, 0, [])],
            }
            if line.product_id:
                res = sols_obj.product_id_change(cr, uid, [], self_so.pricelist_id.id, line.product_id.id, qty=line.product_uom_qty,
                        uom=line.product_uom.id, qty_uos=line.product_uos_qty, uos=line.product_uos and line.product_uos.id or False, name=line.name, partner_id=self_so.partner_id and self_so.partner_id.id or False,
                        lang=False, update_tax=True, date_order=self_so.date_order, packaging=False, fiscal_position=self_so.fiscal_position, flag=False, context=context)
                if res.get('value'):
                    defaults.update(res['value'])
                    if 'tax_id' in defaults:
                        defaults['tax_id'] = [(6,6,defaults['tax_id'])]
            new_id = sols_obj.copy(cr, uid, line.id, defaults, context=context)

        return {}

wiz_copy_so_lines()
