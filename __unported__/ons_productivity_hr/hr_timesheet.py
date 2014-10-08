# -*- coding: utf-8 -*-
#
#  File: hr_timesheet.py
#  Module: ons_productivity_hr
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014 Open-Net Ltd. All rights reserved.
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

from osv import osv,fields
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class hr_timesheet_sheet(osv.osv):
    _inherit = 'hr_timesheet_sheet.sheet'

    def create(self, cr, uid, vals, context=None):
        return super(hr_timesheet_sheet, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, *args, **argv):
        if 'employee_id' in vals:
            new_user_id = self.pool.get('hr.employee').browse(cr, uid, vals['employee_id']).user_id.id or False
            if not new_user_id:
                raise osv.except_osv(_('Error!'), _('In order to create a timesheet for this employee, you must assign it to a user.'))
            if not self._sheet_date(cr, uid, ids, forced_user_id=new_user_id, context={'ons_employee_to_check':vals['employee_id']}):
                raise osv.except_osv(_('Error!'), _('You cannot have 2 timesheets that overlap!\nYou should use the menu \'My Timesheet\' to avoid this problem.'))
            if not self.pool.get('hr.employee').browse(cr, uid, vals['employee_id']).product_id:
                raise osv.except_osv(_('Error!'), _('In order to create a timesheet for this employee, you must link the employee to a product.'))
            if not self.pool.get('hr.employee').browse(cr, uid, vals['employee_id']).journal_id:
                raise osv.except_osv(_('Configuration Error!'), _('In order to create a timesheet for this employee, you must assign an analytic journal to the employee, like \'Timesheet Journal\'.'))
        return super(hr_timesheet_sheet, self).write(cr, uid, ids, vals, *args, **argv)

    def _sheet_date(self, cr, uid, ids, forced_employee_id=False, context=None):
        forced_employee_id = (context or {}).get('employee_id', False)
        for sheet in self.browse(cr, uid, ids, context=context):
            new_employee_id = forced_employee_id or sheet.employee_id and sheet.employee_id.id
            if new_employee_id:
                cr.execute('SELECT id ' +
                    'FROM hr_timesheet_sheet_sheet ' +
                    'WHERE (date_from <= %s and %s <= date_to) ' +
                        'AND employee_id=%s ' +
                        'AND id <> %s',(sheet.date_to, sheet.date_from, new_employee_id, sheet.id))
                if cr.fetchall():
                    return False
        return True


    _constraints = [
        (_sheet_date, 'You cannot have 2 timesheets that overlap!\nPlease use the menu \'My Current Timesheet\' to avoid this problem.', ['date_from','date_to']),
    ]


class hr_timesheet_line(osv.osv):
    _inherit = "hr.analytic.timesheet"
    
    def _sheet(self, cursor, user, ids, name, args, context=None):
        sheet_obj = self.pool.get('hr_timesheet_sheet.sheet')
        res = {}.fromkeys(ids, False)
        for ts_line in self.browse(cursor, user, ids, context=context):
            sheet_ids = sheet_obj.search(cursor, user,
                [('date_to', '>=', ts_line.date), ('date_from', '<=', ts_line.date),
                 ('employee_id', '=', ts_line.employee_id.id)],
                context=context)
            if not sheet_ids:
                sheet_ids = sheet_obj.search(cursor, user,
                    [('date_to', '>=', ts_line.date), ('date_from', '<=', ts_line.date),
                     ('user_id', '=', ts_line.user_id.id)],
                    context=context)
            if sheet_ids:
            # [0] because only one sheet possible for an employee between 2 dates
                res[ts_line.id] = sheet_obj.name_get(cursor, user, sheet_ids, context=context)[0]
        return res

    def _get_hr_timesheet_sheet(self, cr, uid, ids, context=None):
        ts_line_ids = []
        for ts in self.browse(cr, uid, ids, context=context):
            if ts.employee_id:
                cr.execute("""
                        SELECT l.id
                            FROM hr_analytic_timesheet l
                        INNER JOIN account_analytic_line al
                            ON (l.line_id = al.id)
                        WHERE %(date_to)s >= al.date
                            AND %(date_from)s <= al.date
                            AND %(empl_id)s = l.employee_id
                        GROUP BY l.id""", {'date_from': ts.date_from,
                                            'date_to': ts.date_to,
                                            'empl_id': ts.employee_id.id,})
            else:
                cr.execute("""
                        SELECT l.id
                            FROM hr_analytic_timesheet l
                        INNER JOIN account_analytic_line al
                            ON (l.line_id = al.id)
                        WHERE %(date_to)s >= al.date
                            AND %(date_from)s <= al.date
                            AND %(user_id)s = al.user_id
                        GROUP BY l.id""", {'date_from': ts.date_from,
                                            'date_to': ts.date_to,
                                            'user_id': ts.employee_id.user_id.id,})

            ts_line_ids.extend([row[0] for row in cr.fetchall()])
        return ts_line_ids

    def _get_account_analytic_line(self, cr, uid, ids, context=None):
        ts_line_ids = self.pool.get('hr.analytic.timesheet').search(cr, uid, [('line_id', 'in', ids)])
        return ts_line_ids

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        'sheet_id': fields.function(_sheet, string='Sheet', select="1",
            type='many2one', relation='hr_timesheet_sheet.sheet', ondelete="cascade",
            store={
                    'hr_timesheet_sheet.sheet': (_get_hr_timesheet_sheet, ['employee_id', 'date_from', 'date_to'], 10),
                    'account.analytic.line': (_get_account_analytic_line, ['user_id', 'date'], 10),
                    'hr.analytic.timesheet': (lambda self,cr,uid,ids,context=None: ids, None, 10),
                  },
            ),
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('sheet_id', False):
            sheet = self.pool.get('hr_timesheet_sheet.sheet').read(cr, uid, vals['sheet_id'], ['employee_id'], context=context)
            if sheet and sheet.get('employee_id', False):
                vals['employee_id'] = sheet['employee_id'][0]
        return super(hr_timesheet_line, self).create(cr, uid, vals, context=context)

