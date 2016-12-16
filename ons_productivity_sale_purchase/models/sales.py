# -*- coding: utf-8 -*-
#
#  File: models/sales.py
#  Module: ons_productivity_sale_purchase
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open-Net Ltd. <http://www.open-net.ch>

from openerp import fields, models, api

class sale_order(models.Model):
    _inherit = "sale.order"

    purchase_ids = fields.Many2many('purchase.order', compute='_detect_purchase_orders', string='Purchases associated to this sale')
    purchase_count = fields.Integer(string='Buy Orders', compute='_detect_purchase_orders')

    @api.multi
    def _detect_purchase_orders(self):
        for order in self:
            filter = [
                ('group_id', '=', order.procurement_group_id.id)
            ]
            order.purchase_ids = self.env['purchase.order'].search(filter) if order.procurement_group_id else []
            order.purchase_count = len(order.purchase_ids)

    @api.multi
    def action_view_purchases(self):
        '''
        This function returns an action that display existing purchase orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('ons_productivity_sale_purchase.onsp_purchase_form_action')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }

        po_ids = sum([order.purchase_ids.ids for order in self], [])

        if len(po_ids) > 1:
            result['domain'] = "[('id','in',"+str(map(str, po_ids))+")]"
        elif len(po_ids) == 1:
            form = self.env.ref('purchase.purchase_order_form', False)
            form_id = form.id if form else False
            result['views'] = [(form_id, 'form')]
            result['res_id'] = po_ids[0]

        return result
