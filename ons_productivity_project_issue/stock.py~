# -*- coding: utf-8 -*-
#
#  File: stock.py
#  Module: ons_productivity_stock
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

class stock_move(osv.osv):
    _inherit = 'stock.move'

    # ------------------------- Worklfow-related

    def action_done(self, cr, uid, ids, context=None):
        todo = [mv.id for mv in self.browse(cr, uid, ids, context=context) if mv.state not in ['done','cancel']]
        ret = super(stock_move, self).action_done(cr, uid, ids, context=context)
        if todo:
            proc_obj = self.pool.get('procurement.order')
            if proc_obj:
                proc_ids = proc_obj.search(cr, uid, [('state','!=','done'),('move_id','in',todo)], context=context)
                if proc_ids:
                    proc_obj.action_done(cr, uid, proc_ids)
        
        return ret

    # ------------------------- Utility functions
    
    # Used to split the stock_moves
    # the new qty and the corresponding prodlots list may be given by context
    # the qty defaults to 1, and no prodlot is used by default
    def split_move_by(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        new_qty = context.get('Split_by_Q', 1.0)
        if isinstance(ids, (int,long)): ids = [ids]
        
        for mv in self.browse(cr, uid, ids, context=context):
            if mv.product_qty <= 0.0: continue
            
            refs = context.get('Split_with_prodlots', {str(mv.id): []})[str(mv.id)]
            if not refs: continue

            new_uos_qty = new_qty / mv.product_qty * mv.product_uos_qty
            vals = {'product_qty' : new_qty, 'product_uos_qty': new_uos_qty, 'state':mv.state}
            t_i = 0
            while mv.product_qty > new_qty:
                if t_i < len(refs):
                    ref = refs[t_i]
                    if isinstance(ref,(int,long)):
                        vals['prodlot_id'] = ref
                    else:
                        vals.update({
                            'prodlot_id': ref[0],
                            'tracking_id': ref[1],
                        })
                    t_i += 1
                new_obj = self.copy(cr, uid, mv.id, vals)
                mv.product_qty -= new_qty
                vals = {'product_qty' : new_qty, 'product_uos_qty': new_uos_qty, 'state':mv.state}

            if t_i < len(refs):
                ref = refs[t_i]
                if isinstance(ref,(int,long)):
                    vals['prodlot_id'] = ref
                else:
                    vals.update({
                        'prodlot_id': ref[0],
                        'tracking_id': ref[1],
                    })
            self.write(cr, uid, [mv.id], vals)
            
        return True

stock_move()

class stock_production_lot(osv.osv):
    _inherit = 'stock.production.lot'

    # ------------------------- Fields-related functions
    
    def _find_current_location(self, cr, uid, ids, field_name, arg, context=None):
        ret = {}
        for prodlot in self.browse(cr, uid, ids, context=context):
            cr.execute("Select location_dest_id from stock_move where prodlot_id=%d order by date desc limit 1" % prodlot.id)
            res = cr.fetchone()
            ret[prodlot.id] = res and res[0] or False
        
        return ret
    
    def _stock_moves_2_prodlot(self, cr, uid, stock_move_ids, context=None):
        ret = []
        for stock_move in self.pool.get('stock.move').read(cr, uid, stock_move_ids, ['id', 'prodlot_id'], context=context):
            if stock_move.get('prodlot_id', False) and stock_move['prodlot_id'][0] not in ret:
                ret += [stock_move['prodlot_id'][0]]
        
        return ret

    _columns = {
        'current_location_id': fields.function(_find_current_location, method=True, type='many2one', relation='stock.location', string='Current location',
                store = {
                    'stock.move': ( _stock_moves_2_prodlot, ['prodlot_id'], 10 ),
                }),
    }

stock_production_lot()
