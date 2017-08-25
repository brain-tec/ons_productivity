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

    salaire_restant_annualise = fields.Float(string="Salaire Annualisé", compute="_get_annual_salary")
    last_payslip_gross_amount = fields.Float(string="Montant brut du dernier salaire", compute="_get_last_gross_payslip")
    month = fields.Integer(string="Month", compute="_get_month")