# -*- coding: utf-8 -*-
#
#  File: models/hr_timesheet.py
#  Module: ons_productivity_hr_timesheet
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. All rights reserved.
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

class account_analytic_line(osv.osv):
    _inherit = 'account.analytic.line'

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee', select=1),
    }
    
class hr_analytic_timesheet(osv.osv):
    _inherit = 'hr.analytic.timesheet'

    def _ons_getEmployeeProduct(self, cr, uid, context=None):
        if context is None:
            context = {}
        emp_obj = self.pool.get('hr.employee')

        if context.get('employee_id'):
            emp_id = [context.get('employee_id')]
        else:
            emp_id = emp_obj.search(cr, uid, [('user_id', '=', context.get('user_id') or uid)], context=context)
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
            if emp.product_id:
                return emp.product_id.id

        return False

    def _ons_getEmployeeUnit(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        if context is None:
            context = {}

        if context.get('employee_id'):
            emp_id = [context.get('employee_id')]
        else:
            emp_id = emp_obj.search(cr, uid, [('user_id', '=', context.get('user_id') or uid)], context=context)
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
            if emp.product_id:
                return emp.product_id.uom_id.id

        return False

    def _ons_getGeneralAccount(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        if context is None:
            context = {}

        if context.get('employee_id'):
            emp_id = [context.get('employee_id')]
        else:
            emp_id = context.get('employee_id', False)
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id, context=context)
            if bool(emp.product_id):
                a = emp.product_id.property_account_expense.id
                if not a:
                    a = emp.product_id.categ_id.property_account_expense_categ.id
                if a:
                    return a

        emp_id = emp_obj.search(cr, uid, [('user_id', '=', context.get('user_id') or uid)], context=context)
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
            if bool(emp.product_id):
                a = emp.product_id.property_account_expense.id
                if not a:
                    a = emp.product_id.categ_id.property_account_expense_categ.id
                if a:
                    return a

        return False

    def _ons_getAnalyticJournal(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        if context is None:
            context = {}

        if context.get('employee_id'):
            emp_id = [context.get('employee_id')]
        else:
            emp_id = emp_obj.search(cr, uid, [('user_id','=',context.get('user_id') or uid)], limit=1, context=context)
        if not emp_id:
            model, action_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'hr', 'open_view_employee_list_my')
            msg = _("Employee is not created for this user. Please create one from configuration panel.")
            raise openerp.exceptions.RedirectWarning(msg, action_id, _('Go to the configuration panel'))

        emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
        if emp.journal_id:
            return emp.journal_id.id
        else :
            raise osv.except_osv(_('Warning!'), _('No analytic journal defined for \'%s\'.\nYou should assign an analytic journal on the employee form.')%(emp.name))
    
    def on_change_user_id(self, cr, uid, ids, user_id):
        return {}

    def onchange_user_id(self, cr, uid, ids, user_id, context={}):
        if not user_id:
            return {}
        ctx = (context or {}).copy()
        ctx['user_id'] = user_id
        return {'value': {
            'product_id': self. _ons_getEmployeeProduct(cr, uid, ctx),
            'product_uom_id': self._ons_getEmployeeUnit(cr, uid, ctx),
            'general_account_id': self._ons_getGeneralAccount(cr, uid, ctx),
            'journal_id': self._ons_getAnalyticJournal(cr, uid, ctx),
        }}

    def onchange_employee_id(self, cr, uid, ids, employee_id):
        if not employee_id: return {}

        context = {'employee_id': employee_id}
        employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
        if not employee: return {}

        res = {'value':{}}
        if employee.user_id:
            res = self.onchange_user_id(cr, uid, ids, employee.user_id.id, context=context)
            res['value']['user_id'] = employee.user_id.id
        if employee.product_id:
            res['value']['product_id'] = employee.product_id.id
            if employee.product_id.property_account_expense:
                res['value']['general_account_id'] = employee.product_id.property_account_expense.id
            elif employee.product_id.categ_id and employee.product_id.categ_id.property_account_expense_categ:
                res['value']['general_account_id'] = employee.product_id.categ_id.property_account_expense_categ.id
        return res

class hr_timesheet_sheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"

    def _sheet_date(self, cr, uid, ids, forced_user_id=False, context=None):
        return True

    _constraints = [
        (_sheet_date, 'You cannot have 2 timesheets that overlap!\nPlease use the menu \'My Current Timesheet\' to avoid this problem.', ['date_from','date_to']),
    ]
