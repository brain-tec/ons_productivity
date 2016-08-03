# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api


class project_project(models.Model):
    _inherit = 'project.project'

    ons_stage_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', string="Stages")