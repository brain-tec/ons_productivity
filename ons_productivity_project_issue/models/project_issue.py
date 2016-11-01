# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
