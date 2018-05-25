# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CustomerInfo(models.Model):
    _name = "product.customerinfo"
    _description = "Customer information about a product"

    name = fields.Many2one(
        'res.partner', 'Customer',
        domain=[('customer', '=', True)], ondelete='cascade', required=True,
        help="Customer of this product")

    product_name = fields.Char(
        'Customer Product Name',
        help="This customer's product name will be used when printing a quotation/invoice for a customer. Keep empty to use the internal one.")

    product_code = fields.Char(
        'Customer Product Code',
        help="This customer's product code will be used when printing a quotation/invoice for a customer. Keep empty to use the internal one.")

    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        help="If not set, the customer price will apply to all variants of this products.")

    product_template_id = fields.Many2one(
        'product.template', 'Product Template',
        index=True, ondelete='cascade', oldname='product_id')
