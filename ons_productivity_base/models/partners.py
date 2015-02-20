# -*- coding: utf-8 -*-
#
#  File: partners.py
#  Module: ons_productivity_base
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014-TODAY Open-Net Ltd. <http://www.open-net.ch>
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

from openerp.osv import osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def onsp_update_thumbnails(self, cr, uid, ids, context={}):
        partner_ids = ids or self.search(cr, uid, [('image', '!=', False)], context=context)
        while partner_ids:
            self._store_set_values(cr, uid, partner_ids[:1000], ['image_small', 'image_medium'], context=context)
            partner_ids = partner_ids[1000:]
        
        return True

res_partner()
