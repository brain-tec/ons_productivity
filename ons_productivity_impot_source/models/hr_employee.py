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

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    impot_source_rate = fields.Float(compute='_get_impot_source_rate', string="Taux d'impôt à la source")
    impot_ecclesiastique = fields.Boolean(string="Avec l'impôt ecclésiastique ?")
    one_revenue = fields.Boolean(string="Un seul revenu ?")

    @api.multi
    def _get_impot_source_rate(self):
        for employee in self:
            source_rate_employee = []
            tarif_group = []
            nb_child = employee.children + employee.children_student
            if employee.marital == 'single':
                if nb_child > 0:
                    tarif_group.append('H')
                else:
                    tarif_group.append('A')
            elif employee.marital == 'married':
                if employee.one_revenue:
                    tarif_group.append('B')
                else:
                    tarif_group.append('C')
            
            canton = False
            if employee.address_home_id.country_id.code == 'CH':
                if employee.address_home_id.state_id:
                    canton = employee.address_home_id.state_id.code.lower()
            else:
                if employee.address_id.state_id:
                    canton = employee.address_id.state_id.code.lower()
                    if employee.address_home_id.country_id.code == 'DE':
                        if employee.marital == 'single':
                            tarif_group.append('L')
                            tarif_group.remove('A')
            _logger.info(tarif_group)
            if canton:
                source_rates = employee.read_file(
                    canton,
                    employee.contract_id.wage,
                    nb_child, tarif_group,
                    employee.impot_ecclesiastique
                )
                # for source_rate in source_rates:
                #     if source_rate.get('taxed_revenue_from') <= employee.contract_id.wage and source_rate.get('taxed_revenue_to') > employee.contract_id.wage:
                #         source_rate_employee.append(source_rates)
                _logger.info(source_rates)
                if source_rates:
                    employee.impot_source_rate = source_rates[0].get('percent_tax')

    @api.model
    def read_file(self, canton, wage, nb_child, tarif_group, eccles):
        directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        f = open('%s/tar16%s.txt' % (directory_path, canton), 'r')
        lines = f.read().splitlines()
        parsed_lines = []
        for line in lines:
            line_parsed = {}
            record_type = line[0:2]
            if record_type in ['00', '12', '99']:
                continue
            line_parsed['record_type'] = record_type
            # if record_type == '06':
            transaction_type = line[2:3]
            canton = line[4:6]
            code = line[6:16].strip()
            ecclesiastique = (code.find('Y') != -1)
            group = ''
            number_child = 0
            initial_validity_date = datetime.strptime(line[16:24], '%Y%m%d').date()
            taxed_revenue_from = int(line[24:31])
            echellon = int(line[33:40])
            taxed_revenue_to = (taxed_revenue_from - 1) + int(line[33:40])
            amount_tax = int(line[45:54])
            percent_tax = int(line[55:57]) + int(line[57:59])/100.0
            for letter in code:
                if letter in ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'L', 'M', 'N', 'O', 'P']:
                    group = letter
                    break
            for number in code:
                if number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    number_child = int(number)
                    break
            is_admin_barem = (code.find('HE') != -1)
            is_employee_barem = (code.find('ME') != -1)
            line_parsed.update({
                'transaction_type': transaction_type,
                'canton': canton,
                'code': code,
                'ecclesiastique': ecclesiastique,
                'group': group,
                'number_child': number_child,
                'is_admin_barem': is_admin_barem,
                'is_employee_barem': is_employee_barem,
                'initial_validity_date': initial_validity_date,
                'taxed_revenue_from': taxed_revenue_from,
                'taxed_revenue_to': taxed_revenue_to,
                'echellon': echellon,
                'amount_tax': amount_tax,
                'percent_tax': percent_tax
            })
            is_in_group = True
            for group in tarif_group:
                if group not in code:
                    is_in_group = False
            if taxed_revenue_from <= wage and taxed_revenue_to > wage and nb_child == number_child and is_in_group and ecclesiastique == eccles:
                parsed_lines.append(line_parsed)
        return parsed_lines