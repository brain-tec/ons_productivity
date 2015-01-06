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
from itertools import groupby

import logging
_logger = logging.getLogger(__name__)

def group_inv_lines(self, ordered_lines, sortkey):
    """Return lines from a specified invoice grouped by sale order"""
    grouped_lines = []
    for key, valuesiter in groupby(ordered_lines, sortkey):
        group = {}
        group['category'] = key
        group['lines'] = list(v for v in valuesiter)

        if 'amount_untaxed' in key and key.amount_untaxed != 0:
            group['subtotal'] = sum(line.price_subtotal for line in group['lines'])
        grouped_lines.append(group)

    return grouped_lines

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

    def ons_sale_layout_lines(self, cr, uid, ids, invoice_id=None, context=None):
        """
        Returns invoice lines from a specified invoice ordered by sale order. 
        Used in sale_layout module.

        :Parameters:
            -'invoice_id' (int): specify the concerned invoice.
        """
        ordered_lines = self.browse(cr, uid, invoice_id, context=context).ordered_lines
        # We chose to group first by sale order name
        sortkey = lambda x: x.sale_order if x.sale_order else ''

        return group_inv_lines(self, ordered_lines, sortkey)

class account_invoice_lines(models.Model):
    _inherit = 'account.invoice.line'
    
    _columns = {
        'sale_lines': fields.many2many('sale.order.line', 'sale_order_line_invoice_rel', 'invoice_id', 'order_line_id', string='Sale Lines', readonly=True, copy=False),
        'sale_order': fields.related('sale_lines', 'order_id', relation='sale.order', type='many2one', string='Sale order', readonly=True),
    }
