# -*- encoding: utf-8 -*-
#
#  File: wizard/wiz_rebuild_pos_seq.py
#  Module: ons_productivity_sale_layout
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open Net Sàrl. All rights reserved.
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

class wiz_rebuild_pos_seq(osv.osv_memory):
    _name = 'onsp.wiz_rebuild_pos_seq'
    _description = 'Open-Net wizard: rebuild the sequence of the SO/INV lines'
    
    # ---------- Fields management

    _columns = {
        'so_id': fields.many2one('sale.order', 'Sale order'),
        'inv_id': fields.many2one('account.invoice', 'Invoice'),
        'step': fields.integer('Step', required=True),
    }
    
    _defaults = {
        'so_id': lambda s,c,u,ct: ct.get('active_model','') == 'sale.order' and ct.get('active_id', False) or False,
        'inv_id': lambda s,c,u,ct: ct.get('active_model','') == 'account.invoice' and ct.get('active_id', False) or False,
        'step': lambda *a: 10,
    }

    def do_it(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        
        datas = self.browse(cr, uid, ids[0], context=context)
        
        if datas.so_id:
            seq = 0
            for line in datas.so_id.order_line:
                seq += datas.step
                line.write({'sequence': seq}, context=context)

        if datas.inv_id:
            seq = 0
            for line in datas.inv_id.invoice_line:
                seq += datas.step
                line.write({'sequence': seq}, context=context)

        return {}

wiz_rebuild_pos_seq()
