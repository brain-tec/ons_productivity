# -*- coding: utf-8 -*-
# Copyright 2017 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields

import logging

_logger = logging.getLogger(__name__)

class PosCategory(models.Model):
    _inherit = 'pos.category'

    onsp_internal_categ_id = fields.Many2one('product.category', string="Internal category")
        
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        for product in self:
            if product.categ_id:
                pos_categ_id = self.env['pos.category'].search([
                    ('onsp_internal_categ_id', '=', product.categ_id.id)
                ])
                # _logger.info(pos_categ_id)
                if pos_categ_id:
                    product.pos_categ_id = pos_categ_id

class ProductCategory(models.Model):
    _inherit = 'product.category'

    @api.multi
    def sync_with_pos_categ(self):
        for category in self:
            pos_categ_id = self.env['pos.category'].search([
                ('onsp_internal_categ_id', '=', category.id)
            ])
            if not pos_categ_id:
                if category.parent_id:
                    pos_parent_categ_id = self.env['pos.category'].search([
                        ('onsp_internal_categ_id', '=', category.parent_id.id)
                    ])
                    if not pos_parent_categ_id:
                        pos_parent_categ_id = self.env['pos.category'].create({
                            'name': category.parent_id.name,
                            'onsp_internal_categ_id': category.parent_id.id,
                        })
                    self.env['pos.category'].create({
                        'name': category.name,
                        'onsp_internal_categ_id': category.id,
                        'parent_id': pos_parent_categ_id.id
                    })
                else:
                    self.env['pos.category'].create({
                        'name': category.name,
                        'onsp_internal_categ_id': category.id,
                    })
