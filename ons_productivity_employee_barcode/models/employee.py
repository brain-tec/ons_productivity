
# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.http import request
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ons_barcode = fields.Char(string="Barcode")

    @api.model
    def set_employee_barcode(self, barcode):
        _logger.info(barcode)
        request.session['employee_barcode'] = barcode