# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('stage_id', 'timesheet_ids.unit_amount', 'planned_hours', 'child_ids.stage_id',
                 'child_ids.planned_hours', 'child_ids.effective_hours', 'child_ids.children_hours', 'child_ids.timesheet_ids.unit_amount')
    def _hours_get(self):
        super(ProjectTask, self)._hours_get()
        for task in self.sorted(key='id', reverse=True):
            effective_hours = 0
            for timesheet_line in task.timesheet_ids:
                if timesheet_line.ons_to_invoice:
                    effective_hours += timesheet_line.unit_amount

            task.effective_hours = effective_hours
            task.remaining_hours = task.planned_hours - task.effective_hours