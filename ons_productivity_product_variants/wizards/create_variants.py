# -*- coding: utf-8 -*-
#
#  File: wizards/create_variants.py
#  Module: ons_productivity_product_variants
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open Net Sàrl. <http://www.open-net.ch>

from openerp import models, fields, api, _

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
        product_template = self.env['product.template'].browse(self.env.context.get('default_product_template', False))
        if product_template:
            res['product_template'] = product_template.id
            lst = []
            for line in product_template.attribute_line_ids:
                vals = {
                    'product_template': product_template.id,
                    'attribute_id': line.attribute_id.id
                }
                lst.append((0,0,vals))
            res['line_ids'] = lst

        return res

    @api.multi
    def prepare_values(self):
        self.ensure_one()

        variant_ids = [l.value_id.id for l in self.line_ids]
        values = {
            'product_tmpl_id': self.product_template.id,
            'attribute_value_ids': [(6, 0, variant_ids)] if variant_ids else []
        }

        return values

    @api.multi
    def check_unicity(self, values):
#         filter = [('product_tmpl_id','=',values['product_tmpl_id')]
#         if values['attribute_value_ids']:
#             lst = []
#             for l in values['attribute_value_ids'][2]:
#                 item = ()
#                 if not lst:
#                     lst = [(]
#                 filter.append

        return True

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
        for wiz in self:
            values = wiz.prepare_values()
            self.check_unicity(values)
            product = Product.with_context(tracking_disable=True).create(values)
            self.update_product_template()

        return {}
