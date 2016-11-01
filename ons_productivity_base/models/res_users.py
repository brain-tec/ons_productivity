# -*- coding: utf-8 -*-
#
#  File: models/res_users.py
#  Module: ons_productivity_base
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
##############################################################################
#    
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
##############################################################################


from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ResGroups(models.Model):
    _inherit = 'res.groups'

    # ---------- Interface management
    
    @api.v7
    def get_groups_by_application_nada(self, cr, uid, context={}):
        values = super(ResGroups, self).get_groups_by_application(cr, uid, context=context)
        if not (context or {}).get('ons_application_only', False):
            return values
        
        return [x_tuple for x_tuple in values if x_tuple[0]]

class ResUsers(models.Model):
    _inherit = 'res.users'

    # ---------- Interface management

    @api.v7
    def fields_get_nada(self, cr, uid, allfields=None, context=None, write_access=True, attributes=None):
        res = super(ResUsers, self).fields_get(cr, uid, allfields=allfields, context=context, write_access=write_access, attributes=attributes)
        the_list = self.pool['res.groups'].get_groups_by_application(cr, uid, context)
        for app, kind, gs in the_list:
            if app:
                continue
            for g in gs:
                s_grp = 'in_group_' + str(g.id)
                if s_grp in res:
                    del res[s_grp]
        
        return res

    @api.v7
    def read_nada(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        tmp_res = super(ResUsers, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        _logger.info(" *****************  res from read V7: "+str(tmp_res))

        the_grp_list = self.pool['res.groups'].get_groups_by_application(cr, uid, context)
        final_res = []
        for item in tmp_res:
            final_item = {}
            for k in item:
                if k != 'groups_id':
                    final_item[k] = item[k]
                    continue
                lst = []
                for app, kind, gs in the_grp_list:
                    if not app:
                        for g in gs:
                            s_fld = 'in_group_' + str(g.id)
                            if s_fld in self._fields:
                                del self._fields[s_grp]
                            if s_fld in self._columns:
                                del self._columns[s_grp]
                        continue
                    ref_lst = [g.id for g in gs]
                    for i in item['groups_id']:
                        if i in ref_lst:
                            lst.append(i)
                final_item['groups_id'] = lst
            final_res.append(final_item)
        
        return final_res

    @api.v8
    def read_nada(self, fields=None, load='_classic_read'):
        tmp_res = super(ResUsers, self).read(fields=fields, load=load)
        _logger.info(" *****************  res from read V8: "+str(tmp_res))

        the_grp_list = self.pool['res.groups'].get_groups_by_application(self._cr, self._uid, self._context)
        final_res = []
        for item in tmp_res:
            final_item = {}
            for k in item:
                if k != 'groups_id':
                    final_item[k] = item[k]
                    continue
                lst = []
                for app, kind, gs in the_grp_list:
                    if not app:
                        for g in gs:
                            s_fld = 'in_group_' + str(g.id)
                            if s_fld in self._fields:
                                del self._fields[s_grp]
                            if s_fld in self._columns:
                                del self._columns[s_grp]
                        continue
                    ref_lst = [g.id for g in gs]
                    for i in item['groups_id']:
                        if i in ref_lst:
                            lst.append(i)
                final_item['groups_id'] = lst
            final_res.append(final_item)
        
        return final_res
