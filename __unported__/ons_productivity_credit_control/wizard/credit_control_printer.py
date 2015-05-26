# -*- coding: utf-8 -*-
#
#  File: wizard/credit_control_printer.py
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

import base64

from openerp.osv import orm, fields
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class CreditControlPrinter(orm.TransientModel):
    _inherit = 'credit.control.printer'

    _columns = {
        'mark_as_ready': fields.boolean('Mark email lines as ready',
                                       help="Only email lines will be marked."),
        'report_file': fields.binary('Generated Report', readonly=True, filters=['pdf']),
        'name': fields.char('Name', size=32),
    }

    _defaults = {
        'mark_as_ready': True,
        'name': lambda *a: 'credit_control_printer.pdf',
    }

    def _mark_credit_line(self, cr, uid, comms, lines_channel, new_status, context=None):
        line_ids = []
        for comm in comms:
            line_ids += [x.id for x in comm.credit_control_line_ids if x.channel==lines_channel]
        
        _logger.debug(" ****** About to mark %d '%s' credit lines with the new status '%s'" % (len(line_ids), lines_channel, new_status))
        l_obj = self.pool.get('credit.control.line')
        l_obj.write(cr, uid, line_ids, {'state': new_status}, context=context)

        return line_ids

    def print_lines(self, cr, uid, wiz_id, context=None):
        assert not (isinstance(wiz_id, list) and len(wiz_id) > 1), \
            "wiz_id: only one id expected"
        comm_obj = self.pool.get('credit.control.communication')
        if isinstance(wiz_id, list):
            wiz_id = wiz_id[0]
        form = self.browse(cr, uid, wiz_id, context)

        if not form.line_ids and not form.print_all:
            raise orm.except_orm(_('Error'), _('No credit control lines selected.'))

        line_ids = [l.id for l in form.line_ids]
        comms = comm_obj._generate_comm_from_credit_line_ids(cr, uid, line_ids,
                                                             context=context)
        report_file = comm_obj._generate_report(cr, uid, comms, context=context)
        form.write({'report_file': base64.b64encode(report_file), 'state': 'done'})

        if form.mark_as_sent:
            self._mark_credit_line(cr, uid, comms, 'letter', 'sent', context=context)
        if form.mark_as_ready:
            self._mark_credit_line(cr, uid, comms, 'email', 'to_be_sent', context=context)

        return {'type': 'ir.actions.act_window',
                'res_model': 'credit.control.printer',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': form.id,
                'views': [(False, 'form')],
                'target': 'new',
                }
