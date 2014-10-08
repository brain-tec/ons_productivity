# -*- coding: utf-8 -*-
#
#  File: partners.py
#  Module: ons_productivity_base
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

from openerp.osv import osv, fields
from lxml import etree

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'onsp_company_parent_company': fields.boolean('A company may have a parent'),
    }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        result = super(res_partner,self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self.pool.get('ir.values').get_default(cr, uid, self._name, 'onsp_company_parent_company'):
            doc = etree.XML(result['arch'])
            nodes = doc.xpath("//field[@name='parent_id']")
            for node in nodes:
                if node.attrib.get('attrs'):
                    del node.attrib['attrs']
                if node.attrib.get('on_change'):
                    del node.attrib['on_change']
                if node.attrib.get('modifiers'):
                    del node.attrib['modifiers']
            result['arch'] = etree.tostring(doc)

        return result

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        res = super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        if not res or not isinstance(res,list): return res
        if not context.get('default_type', ''): return res
        lst = []
        for item_id,item_name in res:
            if not item_name:
                item_name = ''
            row = self.browse(cr, uid, item_id, context=context)
            if row.use_parent_address and row.parent_id:
                row = row.parent_id
            txt = row.zip or ''
            if row.city:
                if txt:
                    txt += ' '
                txt += row.city
            if item_name:
                txt = ', ' + txt
            lst.append((item_id, item_name + txt))
        
        return lst

res_partner()
