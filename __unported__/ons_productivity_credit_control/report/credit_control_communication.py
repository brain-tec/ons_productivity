# -*- coding: utf-8 -*-
#
#  File: report/credit_control_communication.py
#  Module: ons_productivity_credit_control
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open Net Sàrl. All rights reserved.
##############################################################################
#
#    Author: Nicolas Bessi, Guewen Baconnier
#    Copyright 2012 Camptocamp SA
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
import netsvc
import logging
from openerp.osv.orm import  TransientModel, fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _

logger = logging.getLogger('credit.control.line.mailing')


class CreditCommunication(TransientModel):
    """Shell calss used to provide a base model to email template and reporting.
       Il use this approche in version 7 a browse record will exist even if not saved"""
    _inherit = "credit.control.communication"

    def _generate_report(self, cr, uid, comms, context=None):
        """Will generate a report by inserting mako template of related policy template"""
        service = netsvc.LocalService('report.ons_credit_control_summary')
        ids = [x.id for x in comms]
        result, format = service.create(cr, uid, ids, {}, {})
        return result

