# -*- coding: utf-8 -*-
#
#  File: wizard/credit_control_marker.py
#  Module: ons_productivity_credit_control
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

from openerp.osv import orm, fields
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class CreditControlMarker(orm.TransientModel):
    _inherit = 'credit.control.marker'

    _columns = {
        'name': fields.selection([('draft', 'Draft'),
                                  ('ignored', 'Ignored'),
                                  ('to_be_sent', 'Ready To Send'),
                                  ('sent', 'Done')],
                                  'Mark as', required=True),
    }


