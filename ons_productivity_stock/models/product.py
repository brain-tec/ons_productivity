# -*- coding: utf-8 -*-
# Copyright 2017 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class ProductCategory(models.Model):
    _inherit = "product.category"

    onsp_hs_code = fields.Char(
        string="HS Code", 
        help="Standardized code for international shipping and goods declaration")
    onsp_eccn = fields.Char(
        string="ECCN")
    onsp_country_origin = fields.Many2one(
        'res.country', 
        string='Country of origin')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    onsp_eccn = fields.Char(
        string="ECCN")
    onsp_country_origin = fields.Many2one(
        'res.country', 
        string='Country of origin')
