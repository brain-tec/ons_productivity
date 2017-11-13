# -*- coding: utf-8 -*-
# Copyright 2017 Open Net Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields

import logging

_logger = logging.getLogger(__name__)


class project_project(models.Model):
    _inherit = 'project.project'

    ons_stage_ids = fields.Many2many(
        'project.task.type', 'project_task_type_rel', 'project_id', 'type_id', 
        string="Stages",
        default=lambda self: self._get_default_ons_stage_ids())

    @api.model
    def _get_default_ons_stage_ids(self):
        return self.env['project.task.type'].search([])
