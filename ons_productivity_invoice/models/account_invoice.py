# -*- coding: utf-8 -*-
#
#  File: models/account_invoice.py
#  Module: ons_productivity_invoice
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2014-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
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

from openerp import models, api, _
from openerp.osv import fields

import logging
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    def _get_ordered_lines(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            ail_ids = [x.id for x in record.invoice_line]
            if not ail_ids:
                result[record.id] = []
                continue

            query = 'select solir.invoice_id '\
                    'from sale_order_line_invoice_rel solir '\
                    'left join sale_order_line sol on solir.order_line_id=sol.id '\
                    'inner join sale_order so on so.id=sol.order_id '\
                    'inner join account_invoice_line ail on solir.invoice_id=ail.id '\
                    'where solir.invoice_id in %s '\
                    'order by so.name asc, ail.categ_sequence asc, ail.id asc'
            cr.execute(query, (tuple(ail_ids),))
            result[record.id] = [x[0] for x in cr.fetchall()]
            
        return result
    
    _columns = {
        'ordered_lines': fields.function(_get_ordered_lines, relation='account.invoice.line', type='one2many', string='Sale ordered invoice lines', store=False),
    }

    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'ons_productivity_invoice.report_invoice_by_so')

class account_invoice_lines(models.Model):
    _inherit = 'account.invoice.line'
    
    _columns = {
        'sale_lines': fields.many2many('sale.order.line', 'sale_order_line_invoice_rel', 'invoice_id', 'order_line_id', string='Sale Lines', readonly=True, copy=False),
        'sale_order': fields.related('sale_lines', 'order_id', relation='sale.order', type='many2one', string='Sale order', readonly=True),
    }
