# -*- coding: utf-8 -*-
#
#  File: wizards/create_variants.py
#  Module: ons_productivity_product_variants
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open Net Sàrl. <http://www.open-net.ch>

from openerp import models, fields, api, _
from openerp.exceptions import UserError

class CreateProductLine(models.TransientModel):
    _name = 'onsp_wiz.create.product.line'

    wiz_id = fields.Many2one('onsp_wiz.create.product.product', string='Wizard')
    product_template = fields.Many2one('product.template', string='Template')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    value_id = fields.Many2one('product.attribute.value', string='Value')

class CreateProductVariants(models.TransientModel):
    _name = 'onsp_wiz.create.product.product'

    product_template = fields.Many2one('product.template', string='Template')
    currency_id = fields.Many2one('res.currency', string='Suppler currency',
        related='product_template.main_vendor.ons_supplier_currency')
    line_ids = fields.One2many('onsp_wiz.create.product.line', 'wiz_id', 'Product Attributes')

    @api.model
    def default_get(self, fields_list):
        res = super(CreateProductVariants, self).default_get(fields_list)

        product_variant = self.env['product.product'].browse(self.env.context.get('default_product_variant', False))
        product_template = self.env['product.template'].browse(self.env.context.get('default_product_template', False))
        if product_template:
            res['product_template'] = product_template.id
            lst = []
            for line in product_template.attribute_line_ids:
                vals = {
                    'product_template': product_template.id,
                    'attribute_id': line.attribute_id.id
                }
                if product_variant:
                    for var in product_variant.attribute_value_ids:
                        if var.attribute_id == line.attribute_id:
                            vals['value_id'] = var.id

                lst.append((0,0,vals))

            res['line_ids'] = lst

        return res

    @api.multi
    def prepare_values(self):
        self.ensure_one()

        variant_ids = [l.value_id.id for l in self.line_ids if l.value_id]
        values = {
            'product_tmpl_id': self.product_template.id,
            'attribute_value_ids': [(6, 0, variant_ids)] if variant_ids else []
        }

        return values

    @api.multi
    def check_unicity(self, values):
        unique = True
        query = """select att_id
from product_attribute_value_product_product_rel r, product_product p
where r.prod_id=p.id and p.product_tmpl_id=""" + str(values['product_tmpl_id'])
        self._cr.execute(query)
        existing_lst= [x[0] for x in self._cr.fetchall()]
        if values['attribute_value_ids']:
            new_lst = [x[2][0] for x in values['attribute_value_ids']]
            for item in existing_lst:
                if item in new_lst:
                    new_lst.remove(item)
            if not new_lst:
                unique = False
        else:
            if self.product_template:
                for prod in self.product_template.product_variant_ids:
                    if not prod.attribute_value_ids:
                        unique = False
                        break

        return unique

    @api.multi
    def update_product_template(self):
        self.ensure_one()

        if not self.product_template:
            return False

        values_list = []
        for l in self.product_template.attribute_line_ids:
            values_list.append([v.id for v in l.value_ids])

        for l in self.line_ids:
            if not l.value_id:
                continue
            if l.value_id.id in values_list:
                continue
            for lv in self.product_template.attribute_line_ids:
                if lv.attribute_id == l.attribute_id:
                    lv.value_ids = [(4,l.value_id.id,[])]

        return True

    @api.multi
    def action_create_variant(self):
        Product = self.env['product.product']
        product = False
        for wiz in self:
            values = wiz.prepare_values()
            if not self.check_unicity(values):
                raise UserError("Each variant must be unique")

            product = Product.with_context(tracking_disable=True).create(values)
            self.update_product_template()

        res = self.product_template.action_create_variants()
        if product:
            res['context'].update({
                'default_product_variant': product.id
            })

        return res
