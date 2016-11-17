
# -*- coding: utf-8 -*-

from openerp import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    ons_needs_barcode = fields.Boolean(string="Lock without barcode")