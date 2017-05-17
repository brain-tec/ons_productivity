# -*- coding: utf-8 -*-
#
#  File: models/users.py
#  Module: ons_productivity_dummies
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open-Net Ltd. All rights reserved.

from odoo import api, fields, models

class Users(models.Model):
    _inherit = 'res.users'

    share = fields.Boolean(compute='_compute_share', compute_sudo=True, string='Share User', store=True,
         help="External user with limited access, created only for the purpose of sharing data.")

    @api.depends('groups_id')
    def _compute_share(self):
        ICP = api.Environment(self._cr, self._uid, {})['ir.config_parameter']
        dummies_group = ICP.get_param('ons.dummies.group', 85)

        for user in self:
            self._cr.execute("SELECT 1 FROM res_groups_users_rel WHERE uid=%s AND gid=%s",
                    (self._uid, str(dummies_group)))
            user.share = not bool(self._cr.fetchone())

