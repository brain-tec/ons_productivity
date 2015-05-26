# -*- coding: utf-8 -*-
#
#  File: config/config.py
#  Module: ons_productivity_acc_stmt
#  Config management
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open Net Sàrl. All rights reserved.
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
from operator import itemgetter

ons_module_params_description = 'Account statement parameters'
ons_module_params_name = 'ons.account_statement.params'
ons_module_settings_name = 'ons.account_statement.settings'

class ons_module_params(osv.osv):
    _name = ons_module_params_name
    _description = ons_module_params_description

    # ------------------------- Fields related
    
    _columns = {
        'name': fields.char('Name', size=64),

        'directory_in': fields.char('Input', size=200),
        'directory_out': fields.char('Output', size=200),
        'file_name_mask': fields.char('File name mask', size=50),
        'last_imported_file': fields.char('Last imported file', size=200, readonly=True),
        'ref_mask': fields.char('Ref mask', size=100),
    }
    
    _defaults = {
        'name': lambda *a: ons_module_params_description,
    }
    
    # ------------------------- Instance handling

    def create(self, cr, uid, vals, context={}):
        context = context or {}
        lst = self.search(cr, uid, [])
        if not lst:
            return super(ons_module_params, self).create(cr, uid, {'name':'Account statement parameters'})
        
        return lst[0]

    def unlink(self, cr, uid, ids, context={}):
        if count(self.search(cr, uid, [])) > 1:
            return super(ons_module_params, self).unlink(cr, uid, ids, context=context)
        
        return False

    def copy(self, cr, uid, id, default={}, context={}):
        raise osv.except_osv(_('Forbidden!'), _('One and only one record for the parameters.'))
    
    def get_instance( self, cr, uid, context={} ):
        for params in self.browse( cr, uid, self.search( cr, uid, [], context=context ), context=context ):
            return params
    
        return False

ons_module_params()

class ons_module_settings(osv.osv):
    _name = ons_module_settings_name
    _inherit = 'res.config.settings'

    # ---------- Fields management

    _columns = {
        'directory_in': fields.char('Input', size=200),
        'directory_out': fields.char('Output', size=200),
        'file_name_mask': fields.char('File name mask', size=50),
        'last_imported_file': fields.char('Last imported file', size=200, readonly=True),
        'ref_mask': fields.char('Ref mask', size=100),
    }

    _defaults = {
    }

    # ---------- Instances management
    
    def copy_vals(self, rec):
        ret = {}
        for fname, field in self._columns.iteritems():
            if isinstance(field,(fields.related,fields.one2many,fields.many2many,fields.sparse,fields.function,fields.dummy,fields.serialized,fields.property)):
                continue
            if isinstance(field,fields.many2one):
                if rec.get(fname, False):
                    ret[fname] = rec[fname][0]
                continue
            ret[fname] = rec[fname]
        
        return ret

    def default_get(self, cr, uid, fields, context=None):
        cfg_param_obj = self.pool.get(ons_module_params_name)
        ids = cfg_param_obj.search(cr, uid, [], context=context)
        if not ids:
            return {}
        rec = cfg_param_obj.read(cr, uid, ids[0], [], context=context)
        if not rec:
            return {}
        
        ret = self.copy_vals(rec)
        if ret.get('date_format', False):
            ret['date_format'] = '%d.%m.%Y'
        return ret

    def execute(self, cr, uid, ids, context=None):
        cfg_param_obj = self.pool.get(ons_module_params_name)

        rec = self.read(cr, uid, ids[0], [], context)
        vals = self.copy_vals(rec)

        rec_ids = cfg_param_obj.search(cr, uid, [], context=context)
        if not rec_ids:
            vals['name'] = ons_module_params._description
            rec_id = cfg_param_obj.create(cr, uid, vals, context=context)
        else:
            rec_id = rec_ids[0]
            cfg_param_obj.write(cr, uid, [rec_id], vals, context=context)

        # force client-side reload (update user menu and current view)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

ons_module_settings()
 
