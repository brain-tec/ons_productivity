# -*- coding: utf-8 -*-
#
#  File: wizard/wiz_gen_stats.py
#  Module: ons_productivity_stats
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

from osv import fields, osv
from datetime import *
from dateutil.relativedelta import relativedelta

class wiz_gen_stats(osv.osv_memory):
    _name = 'ons.wiz_gen_stats'
    _description = "Statistics: generate the stats"

    # ------------ Fields management

    _columns = {
        'name': fields.many2one('ons.stats', 'Name', required=True),
        'date_from': fields.date('From', required=True),
        'date_to': fields.date('To', required=True),
    }
    
    _defaults = {
        'name': lambda s,c,u,ct: ct.get('active_id', False),
        'date_from': lambda *a: (datetime.now() - relativedelta(days=7)).strftime('%Y-%m-%d'),
        'date_to': lambda *a: datetime.now().strftime('%Y-%m-%d'),
    }

    # ------------ User interface related

    def do_generate(self, cr, uid, ids, context=None):
        if not ids: return False
        datas = self.browse(cr, uid, ids[0], context=context)
        if not datas: return False
        
        template_id = context.get('active_id')
        new_id = self.pool.get('ons.stats').do_generate(cr, uid, template_id, datas.date_from, datas.date_to, context=context)
        
#         mod_obj = self.pool.get('ir.model.data')
#         act_obj = self.pool.get('ir.actions.act_window')
#         if context is None:
#             context = {}
#         result = mod_obj.get_object_reference(cr, uid, 'ons_productivity_stats', 'ons_stats_list_action')
#         id = result and result[1] or False
#         result = act_obj.read(cr, uid, [id], context=context)[0]
#         result['domain'] = str()
        domain = [('id','=',new_id)]

        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'ons.stats',
            'views': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': domain,
        }

wiz_gen_stats()
