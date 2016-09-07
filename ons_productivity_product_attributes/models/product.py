# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _order = 'attribute_id'