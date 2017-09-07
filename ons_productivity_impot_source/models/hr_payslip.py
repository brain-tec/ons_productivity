# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import fields, models, api
import logging
#Get the logger
_logger = logging.getLogger(__name__)
import os
import inspect

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def _get_month(self):
        for payslip in self:
            payslip.month = fields.Date.from_string(payslip.date_from).month

    @api.multi
    def _get_annual_salary(self):
        for payslip in self:
            payslip.salaire_restant_annualise = payslip.contract_id.wage*(13 - payslip.month +1)

    def _get_last_gross_payslip(self):
        for payslip in self:
            payslips = self.search([('employee_id', '=', payslip.employee_id.id),('id', '!=', payslip.id)])
            last_payslip = False
            for past_payslip in payslips:
                if past_payslip.month == payslip.month-1:
                    last_payslip = past_payslip
            if last_payslip:
                payslip.last_payslip_gross_amount = sum([line.amount for line in last_payslip.line_ids if line.category_id.code == 'GROSS'])

    def _get_last_imp_src(self):
        for payslip in self:
            payslips = self.search([('employee_id', '=', payslip.employee_id.id),('id', '!=', payslip.id)])
            last_payslip = False
            last_payslip_imp_src = 0
            for past_payslip in payslips:
                if past_payslip.month <= payslip.month:
                    last_payslip_imp_src += sum([line.amount for line in past_payslip.line_ids if line.code == 'IMP_SRC'])

            payslip.last_payslip_imp_src = last_payslip_imp_src

    def _get_imp_amount(self):
        for payslip in self:
            payslips = self.search([('employee_id', '=', payslip.employee_id.id),('id', '!=', payslip.id)])
            last_payslip = False
            last_payslip_imp_amount = 0
            for past_payslip in payslips:
                if past_payslip.month < payslip.month:
                    last_payslip_imp_amount += sum([line.amount for line in past_payslip.line_ids if line.category_id.code == 'BASIC' or line.category_id.code == 'ALW' or line.category_id.code == 'ALW_ANU'])
            payslip.last_payslip_imp_amount = last_payslip_imp_amount

    salaire_restant_annualise = fields.Float(string="Salaire Annualisé", compute="_get_annual_salary")
    last_payslip_gross_amount = fields.Float(string="Montant brut du dernier salaire", compute="_get_last_gross_payslip")
    last_payslip_imp_src = fields.Float(string="Montant cummulé des derniers impôts à la source", compute="_get_last_imp_src")
    last_payslip_imp_amount = fields.Float(string="Cummul imposable", compute="_get_imp_amount")
    month = fields.Integer(string="Month", compute="_get_month")