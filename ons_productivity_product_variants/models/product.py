# -*- coding: utf-8 -*-
#
#  File: models/product.py
#  Module: ons_productivity_product_variants
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2016-TODAY Open Net Sàrl. <http://www.open-net.ch>

from openerp import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ---------- Fields management

    force_variants_upt = fields.Boolean('Force variants update')
    main_vendor = fields.Many2one('res.partner', compute='_compute_suppl_infos', string='Vendor')
    min_qty = fields.Float(compute='_compute_suppl_infos', string='Min qty')

    @api.multi
    def _compute_suppl_infos(self):
        for prod in self:
            prod.main_vendor = prod.seller_ids[0].name if prod.seller_ids else False
            prod.min_qty = prod.seller_ids[0].min_qty if prod.seller_ids else 0

    # ---------- Instances management

    @api.multi
    def create(self, vals):
        new_env = self
        if not vals.get('force_variants_upt', False):
            new_env = self.with_context(create_product_variant=True)
        else:
            vals['force_variants_upt'] = False

        return super(ProductTemplate, new_env).create(vals)

    @api.multi
    def write(self, vals):
        new_env = self
        if not vals.get('force_variants_upt', False):
            new_env = self.with_context(create_product_variant=True)
        else:
            vals['force_variants_upt'] = False

        return super(ProductTemplate, new_env).write(vals)

    @api.multi
    def unlink(self):
        return super(ProductTemplate, self).unlink()

    # ---------- Interface management

    @api.multi
    def action_create_variants(self):
        imd = self.env['ir.model.data']
        form_view_id = imd.xmlid_to_res_id('ons_productivity_product_variants.onsp_wiz_create_product_product')
        return {
            'name': _("Create variants"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'onsp_wiz.create.product.product',
            'views': [(form_view_id, 'form')],
            'view_id': form_view_id,
            'target': 'new',
            'context': {'default_product_template':self.id},
        }

    @api.onchange('attribute_id')
    def change_attribute(self):
        if not self.env.context.get('ons_add_values', False):
            return {}

        line = self.env['product.attribute.line'].search(['product_tmpl_id','=',self.env.context.get('active_id', False), ('attribute_id','=',self.attribute_id)])
        if line:
            self.value_ids = line.value_ids


class ProductProduct(models.Model):
    _inherit = 'product.product'

   # ---------- Instances management

    @api.multi
    def unlink(self):
        return super(ProductProduct, self).unlink()


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    @api.onchange('attribute_id')
    def change_attribute(self):
        if not self.env.context.get('ons_add_values', False) or not self.attribute_id:
            return {}

        values = self.env['product.attribute.value'].search([('attribute_id','=',self.attribute_id.id)])
        if values:
            self.value_ids = [v.id for v in values]
