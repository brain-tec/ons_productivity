# -*- coding: utf-8 -*-
#
#  File: wizard/wiz_move_splitter.py
#  Module: ons_productivity_stock
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
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

import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

import csv
import base64

class wiz_move_splitter(osv.osv_memory):
    _name = 'ons.wiz.move_splitter'
    _description = 'Open-Net wizard: move splitter'

    # ------------------------- Fields-related functions
    
    def _get_stock_moves(self, cr, uid, context=None):
        stock_move_obj = self.pool.get( 'stock.move' )
        stock_move_ids = stock_move_obj.search( cr, uid, [('picking_id','=', context.get('active_id',-1))], context=context )
        res = []
        for stock_move_id in stock_move_ids:
            stock_move = stock_move_obj.read( cr, uid, stock_move_id, ['name','product_qty', 'state'])
            if stock_move and stock_move['product_qty'] > 0: # and stock_move['state'] == 'assigned':
                res.append( (stock_move_id, stock_move['name'] + ' (q=%d)' % round(stock_move['product_qty']) ) )
        return res

    _columns = {
        'move_id': fields.selection( _get_stock_moves, method=True, string='Moves' ),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'nb_moves': fields.integer('Nb'),
        'line_count':  fields.integer('Nb serial nbs'),
        'prodlot_ids': fields.many2many( 'stock.production.lot', 'ons_rel_wiz_move_splitter_prodlot', 'wiz_id', 'prodlot_id', string='Serial numbers' ),
        
        'delimiter': fields.char('Delimiter', size=1),
        'mv_split_fname': fields.binary('Select a file', filters='*.csv'),

        # Set by the configuration system ( -> res_config )
        'onsp_stk_split_move_by_file': fields.boolean("Split by file"),
    }
    
    def find_default_move(self, cr, uid, context=None):
        lst = self._get_stock_moves(cr, uid, context=context)
        return lst and lst[0] or False
    
    _defaults = {
        'move_id': find_default_move,
        'onsp_stk_split_move_by_file': lambda s,c,u,ct: s.pool.get('ir.values').get_default(c, u, 'ons.wiz.move_splitter', 'onsp_stk_split_move_by_file'),
        'delimiter': lambda *a: ';',
    }
    
    # ------------------------- Utility functions
    
    def file2list(self, cr, uid, f_content):
        if '\r\n' in f_content:
            return f_content.split('\r\n')
        if '\n\r' in f_content:
            return f_content.split('\n\r')
        if '\n' in f_content:
            return f_content.split('\n')
        if '\r' in f_content:
            return f_content.split('\r')
        
        return [f_content]
    
    def on_change_move(self, cr, uid, ids, move_id):
        if not move_id: return { 'value': { 'prodlot_ids': [(6,0,[])], 'product_id': False } }
        
        move_obj = self.pool.get('stock.move')
        move = move_obj.browse(cr, uid, move_id)
        
        prodlot_obj = self.pool.get('stock.production.lot')
        filters = [('product_id','=',move.product_id.id),('stock_available','>',0)]
        prodlot_ids = prodlot_obj.search(cr, uid, filters)

        vals = { 
            'prodlot_ids': [(6,0,prodlot_ids)], 
            'product_id': move.product_id.id, 
            'nb_moves': round(move.product_qty) 
        }

        return { 'value': vals }

    def on_change_mv_split_fname(self, cr, uid, ids, mv_split_fname, delimiter, nb_moves, context={}):
        if not mv_split_fname or not delimiter: return False
        f_content = self.file2list(cr, uid, base64.decodestring(mv_split_fname))
        lines = csv.reader(f_content, delimiter=str(delimiter))
        
        count = 0
        for ln in lines:
            if not len(ln): 
                continue
            if ln[0][:1] == "#" or ln[0][:1] == " ":
                continue
            count += 1

        ret = { 'value': {'line_count': max(count-1,0)} }
        if nb_moves+1 != count:
            ret['warning'] = {
                'title': _('Remark'), 
                'message' : _('The file must have exactly %d lines,\nthe 1st with the column names,\ninstead of %d') % (nb_moves+1,count)
            }

        return ret
    
wiz_move_splitter()

class wiz_in_move_splitter(osv.osv_memory):
    _name = 'ons.wiz.in_move_splitter'
    _inherit = 'ons.wiz.move_splitter'
    
    # ------------------------- Interface-related functions
    
    def do_split(self, cr, uid, ids, context={}):
        wiz = self.browse(cr, uid, ids[0], context=context)
        if wiz.onsp_stk_split_move_by_file:
            if not wiz.mv_split_fname or not wiz.delimiter: return False
            f_content = self.file2list(cr, uid, base64.decodestring(wiz.mv_split_fname))
            lines = csv.reader(f_content, delimiter=str(wiz.delimiter))
            
            track_obj = self.pool.get('stock.tracking')
            
            count = 0
            lst = []
            for ln in lines:
                if not len(ln): 
                    continue
                if ln[0][:1] == "#" or ln[0][:1] == " ":
                    continue
                if count == 0: 
                    count = 1
                    continue
                count += 1
                mv = self.pool.get('stock.move').read(cr, uid, int(wiz.move_id), ['product_id'], context=context)
                vals = {
                    'name': ln[0],
                    'product_id': mv['product_id'][0],
                    'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                id1 = self.pool.get('stock.production.lot').create(cr, uid, vals, context=context)
                if len(ln) > 1:
                    id2 = track_obj.search(cr, uid, [('name','=',ln[1])], context=context)
                    if id2:
                        id2 = id2[0]
                    else:
                        vals = {
                            'name': ln[1],
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        id2 = track_obj.create(cr, uid, vals, context=context)
                    lst.append([id1,id2])
                else:
                    lst.append(id1)
            
            if not lst:
                return False
            
            ctx = context.copy()
            ctx.update({ 'Split_by_Q':1.0, 'Split_with_prodlots': { wiz.move_id: lst }})
            
        else:
            ctx = context.copy()
            ctx.update({ 'Split_by_Q':1.0, 'Split_with_prodlots': { wiz.move_id: [x.id for x in wiz.prodlot_ids] }})
        
        return self.pool.get('stock.move').split_move_by(cr, uid, [int(wiz.move_id)], context=ctx)

wiz_in_move_splitter()

class wiz_int_out_move_splitter(osv.osv_memory):
    _name = 'ons.wiz.int_out_move_splitter'
    _inherit = 'ons.wiz.move_splitter'

    # ------------------------- Columns related
    
    _columns = {
        'move_ids': fields.many2many( 'stock.move', 'ons_rel_wiz_move_splitter_move', 'wiz_id', 'move_id', string='Moves' ),
    }

    # ------------------------- Utility functions
    
    def on_change_move(self, cr, uid, ids, move_id):
        if not move_id: return { 'value': { 'prodlot_ids': [(6,0,[])], 'product_id': False } }
        
        move_obj = self.pool.get('stock.move')
        move = move_obj.browse(cr, uid, move_id)

        vals = { 
            'product_id': move.product_id.id, 
            'nb_moves': round(move.product_qty) 
        }

        return { 'value': vals }

    def on_change_mv_split_fname(self, cr, uid, ids, mv_split_fname, delimiter, move_id, nb_moves, context={}):
        if not mv_split_fname or not delimiter: return False
        f_content = self.file2list(cr, uid, base64.decodestring(mv_split_fname))
        lines = csv.reader(f_content, delimiter=str(delimiter))
        
        move_obj = self.pool.get('stock.move')
        move = move_obj.browse(cr, uid, move_id)

        count = 0
        move_ids = []
        first_pass = True
        for ln in lines:
            if not len(ln): 
                continue
            if ln[0][:1] == "#" or ln[0][:1] == " ":
                continue
            if first_pass:
                # first line should have the column names: it's skipped
                first_pass = False
                continue

            filters = [
                ('product_id','=',move.product_id.id),
                ('location_dest_id','=',move.location_id.id),
                ('state','=','done'),
                ('tracking_id.name','=',ln[0].strip()),
            ]
            if len(ln) > 1 and ln[1].strip():
                filters += [
                    ('prodlot_id.name','=',ln[1].strip()),
                ]
            found_move_ids = move_obj.search(cr, uid, filters, order='date desc')
            move_ids += found_move_ids
            count += len(found_move_ids)
        
        ret = { 'value': {'line_count': max(count-1,0), 'move_ids': [(6,0,move_ids)]} }
        if nb_moves != count:
            ret['warning'] = {
                'title': _('Remark'), 
                'message' : _('The file provides %d serial numbers,instead of %d') % (count, nb_moves)
            }

        return ret
    
    # ------------------------- Interface-related functions
    
    def do_split(self, cr, uid, ids, context={}):
        wiz = self.browse(cr, uid, ids[0], context=context)

        lst = [ (mv.prodlot_id.id, mv.tracking_id.id) for mv in wiz.move_ids if mv.prodlot_id and mv.tracking_id ]
        ctx = context.copy()
        ctx.update({ 'Split_by_Q':1.0, 'Split_with_prodlots': { wiz.move_id: lst }})
        
        return self.pool.get('stock.move').split_move_by(cr, uid, [int(wiz.move_id)], context=ctx)

wiz_int_out_move_splitter()

