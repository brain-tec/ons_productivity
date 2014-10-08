# -*- coding: utf-8 -*-
#
#  File: wizard/setup_budget_periods.py
#  Module: ons_productivity_budget
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class setup_budget_periods( osv.osv ):
    _name = 'onsp.wiz.setup_budget_periods'
    _description = 'Open-Net wizard: setup budget periods'
    
    # ---------- Fields management

    _columns = {
        'nb_periods': fields.integer( "Nb. periods", required=True ),
    }
    
    _defaults = {
        'nb_periods': lambda s,c,u,ct: s.pool.get('ir.values').get_default(c, u, 'onsp.wiz.setup_budget_periods', 'nb_periods'),
    }

    # ---------- Interface related
    
    def do_it(self, cr, uid, ids, context={}):
        datas = self.browse(cr, uid, ids[0], context=context)
        budget_pos = self.pool.get('onsp.budget.position').browse(cr, uid, context['active_id'], context=context)
        if not budget_pos: return False
        
        period_obj = self.pool.get('onsp.budget.position.period')
        lst = [x.id for x in budget_pos.period_ids]
        if lst:
            period_obj.unlink(cr, uid, lst, context=context)
        period_amount = budget_pos.amount / float(datas.nb_periods)
        format = datas.nb_periods < 10 and '%d' or '%02d'
        lst = []
        for i in range(1,datas.nb_periods+1):
            vals = {
                'name': format % i,
                'amount': period_amount,
                'pos_id': budget_pos.id,
            }
            new_id = period_obj.create(cr, uid, vals, context=context)
            lst.append(new_id)
        budget_pos.write({'nb_periods':datas.nb_periods}, context=context)
            
        return {'type': 'ir.actions.act_window_close'}
        
setup_budget_periods()
