# -*- coding: utf-8 -*-
#
#  File: project_issue.py
#  Module: ons_productivity_project_issue
#
#  Created by sge@open-net.ch
#
#  Copyright (c) 2014 Open Net Sàrl. All rights reserved.
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api


class project_issue(models.Model):
    _inherit = 'project.issue'

    @api.model
    def create(self, vals):
        """
        Overload the original create methode to 
        add the ID of issue on its name
        """
        issues = super(project_issue, self).create(
           vals)

        for issue in issues:
            prefix = "[%s] " % issue.id
            if not prefix in issue.name:
                new_name = prefix + issue.name
                issue.write({'name': new_name})

        return issues

    @api.multi
    def _comp_short_name(self):
        for issue in self:
            short_name = issue.name
            prefix = "[%s] " % issue.id
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix):]
            self.short_name = short_name
    
    short_name = fields.Char(compute=_comp_short_name, string='Short name')
    ons_progress = fields.Float(string="Progress (%)", related="task_id.progress")
