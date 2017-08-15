# -*- coding: utf-8 -*-
#
#  File: wizards/print_task_report.py
#  Module: ons_productivity_project_issue
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2017-TODAY Open Net Sàrl. <http://www.open-net.ch>

from odoo import api, fields, models


class WizPrintTaskReport(models.Model):
    _name = 'onsp.wiz.print_task_report'
    _description = "Open Net Productivity Wizard: print task report"

    # ---------- Fields management

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')

    # ---------- Interface management

    @api.multi
    def action_print_report(self):
        for wiz in self:
            rec = self.env[self.env.context['active_model']].browse(self.env.context['active_id'])
            data = {
                'filter_date_from': wiz.date_from or False,
                'filter_date_to': wiz.date_to or False
            }
            # Write back to the select project task
            task = self.env[self._context['active_model']].browse(self._context['active_id'])
            task.update(data)

            return self.env['report'].get_action(rec, 'ons_productivity_project_issue.report_task_filtered')


        return {}
