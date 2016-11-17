
# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.http import request
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        if request.session.get('employee_barcode'):
            barcode = request.session.get('employee_barcode')
            employees = self.env['hr.employee'].search([('ons_barcode', '=', barcode)])
            if employees:
                if values.get('body'):
                    values['body'] = "%s<br/>%s" % (values['body'], employees[0].name)
                else:
                    values['body'] = employees[0].name
        res = super(Message, self).create(values)
        return res