# -*- coding: utf-8 -*-
#
#  File: wizard/wiz_import_account_statements.py
#  Module: ons_productivity_acc_stmt
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
import base64
import glob
import os

import logging
_logger = logging.getLogger(__name__)

def _get_filenames(self, cr, uid, context={}):
    params = self.pool.get('ons.account_statement.params').get_instance(cr, uid, context=context)
    if not params or not params.directory_in or not params.file_name_mask:
        return []
    
    path = params.directory_in
    if path[-1:] != os.sep:
        path += os.sep
    path += params.file_name_mask
    ref = params.last_imported_file or ''
    return [(x,x.split(os.sep)[-1]) for x in glob.glob(path) if x > ref]

class wiz_import_acc_stmt(osv.osv_memory):
    _name = 'ons.wiz_import_acc_stmt'
    _description = 'Open-Net wizard: import a text file with account statements'

    # ------------------------- Fields related
    
    _columns = {
        'file': fields.binary('File', filters='*.*', required=True),
        'filename': fields.selection(_get_filenames, 'File name'),
    }
    
    def do_it(self, cr, uid, ids, context=None):
        
        if not context:
            context = {}
        
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            f_content = base64.decodestring(obj.file)
            self.pool.get('ons.account_statement').import_mt940(cr, uid, False, f_content.split('\n'), context=context)

        res = {
            'domain': str([]),
            'name': _('Account statements'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'ons.account_statement',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
        return res

wiz_import_acc_stmt()
