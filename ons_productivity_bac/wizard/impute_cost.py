# -*- encoding: utf-8 -*-
#
#  File: wizard/__init__.py
#  Module: ons_productivity_bac
#
#  Copyright (c) 2015-TODAY Open-Net Ltd. <http://www.open-net.ch>
##############################################################################
#
#    Author Joel Grand-Guillaume. Copyright Camptocamp SA
#    Ported to Odoo V8 by cyp@open-net.ch
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _

class impute_cost(osv.TransientModel):
    _name = 'ons.impute.cost'
    _description = 'Impute Analytical Cost'

    _columns = {
        'journal_id' : fields.many2one('account.analytic.journal', 'Analytic Journal', required=True),
        'pickings_ids' : fields.many2many('stock.picking','impute_cost_picking_rel', 'impute_id', 'picking_id', 'Packing'),
    }

    def default_get(self, cr, uid, fields, context={}):
        """ Get the available packing to proceed
        """
        res = super(impute_cost, self).default_get(cr, uid, fields, context=context)

        picking_obj = self.pool.get('stock.picking')
        filter = [
            ('picking_type_id.code','in',['incoming','outgoing']),
            ('state','=','done'),
            ('cost_imputed','=',False),
            ('analytic_cost_id','<>',False)
        ]
        delivery_ids = picking_obj.search(cr, uid, filter, context=context)
        res.update({'pickings_ids':delivery_ids})

        return res

    def on_change_unit_amount(self, cr, uid, id, prod_id, unit_amount,
            unit=False,date_currency=False, context=None):
        uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        currency_obj = self.pool.get('res.currency')
#        if unit_amount and prod_id:
        if  prod_id:
            prod = product_obj.browse(cr, uid, prod_id)
            a = prod.product_tmpl_id.property_account_expense.id
            if not a:
                a = prod.categ_id.property_account_expense_categ.id
            if not a:
                raise osv.except_osv(_('Error !'),
                        _('There is no expense account defined ' \
                                'for this product: "%s" (id:%d)') % \
                                (prod.name, prod.id,))
            if prod.standard_price:
                amount = unit_amount * uom_obj._compute_price(cr, uid,
                        prod.uom_id.id, prod.standard_price, unit)
            else:
                amount = unit_amount * uom_obj._compute_price(cr, uid,
                        prod.uom_id.id, prod.euro_price, unit)
                ## Search currency id for euro
                euro_currency_id = currency_obj.search(cr, uid, [('name', '=', 'EUR')])[0]
                ##
                ## Search currency id for euro
                chf_currency_id = currency_obj.search(cr, uid, [('name', '=', 'CHF')])[0]
                ##
                context_date = {
                'date' : date_currency,
                }
                amount = currency_obj.compute(cr, uid, euro_currency_id, chf_currency_id, amount,context=context_date)
                
            return {'value': {
                'amount': - round(amount, 2),
                'general_account_id': a,
                }}
        return {}

    def _create_analytic_lines(self, cr, uid, moves_obj, journal, type_pack='out', context=None):
        aal_obj = self.pool.get('account.analytic.line')
        aal_created_ids=[]
        for move in moves_obj:
            new_aal={
                'name' : move.picking_id.name + ' - Move ' + move.name,
                'account_id' : move.picking_id.analytic_cost_id.id,
                'product_id' : move.product_id.id,
                'unit_amount' : move.product_qty,
                'product_uom_id' : move.product_uom.id,
                'journal_id' : journal.id,
            }
            if '(return)' in move.picking_id.name:
                new_aal['unit_amount'] = -move.product_qty
            on_change=self.on_change_unit_amount(cr, uid, 1, move.product_id.id, move.product_qty, move.product_uom.id,move.picking_id.date_done, context)
            self.pool.get('stock.move').write(cr, uid, [move.id], { 'ons_pu': on_change['value']['amount'] / (move.product_qty or 1.0) }, context=context)
            if type_pack=='out':    
                amount = on_change['value']['amount']
            else:
                amount = -(on_change['value']['amount'])
            new_aal.update({
                'amount' : amount,
                'general_account_id' : on_change['value']['general_account_id'],
            })
            aal_created_ids.append(aal_obj.create(cr, uid, new_aal, context))
        return aal_created_ids
        
    def impute(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        move_obj = self.pool.get('stock.move')
        delivery_obj = self.pool.get('stock.picking')
        aal_created_ids=[]
        impute_cost_wiz_obj = self.browse(cr, uid, ids)[0]
        deliveries = impute_cost_wiz_obj.pickings_ids
        journal = impute_cost_wiz_obj.journal_id
        # For all Delivery order, for all stock.move
        for delivery in deliveries:
            if not delivery.analytic_cost_id:
                raise osv.except_osv(_("Error"), _("The packing %s has no analytic account !" %(delivery.name)))
            if delivery.cost_imputed:
                raise osv.except_osv(_("Error"), _("The packing  %s has already generated the analytical entries !" %(delivery.name)))
            # Control all moves to see if they contain Customer location
            out_moves=[]
            in_moves=[]
            for move in delivery.move_lines:
                # Move goes out to the customer locations
                if move.location_dest_id.usage == 'customer':
                    out_moves.append(move)
                # Move comes from the customer locations                    
                elif move.location_id.usage == 'customer':
                    in_moves.append(move)
                else:
                    raise osv.except_osv(_("Error"), _("The packing %s has lines that don't come or go to a customer location type !" %(delivery.name)))
            # The delivery order and his line are alright, generate analytic entries
            aal_created_ids += self._create_analytic_lines(cr,uid,out_moves,journal,'out', context)
            aal_created_ids += self._create_analytic_lines(cr,uid,in_moves,journal, 'in', context)
            # Set the delivery order as generated
            delivery_obj.write(cr, uid, [delivery.id], {'cost_imputed':True}, context=context)
        res =  {
            'name': _("Generated Analytics Lines"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.analytic.line',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': "[('id', 'in', %s)]" % aal_created_ids,
        }
            
        return res

impute_cost()
