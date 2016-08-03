# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api


class project_settings(models.TransientModel):
    _inherit = 'project.config.settings'

    ons_default_stage_ids = fields.Many2many(string="Default stages", 'project.task.type')