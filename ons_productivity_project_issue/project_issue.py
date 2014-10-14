# -*- coding: utf-8 -*-
#
#  File: project_issue.py
#  Module: ons_productivity_project_issue
#
#  Created by sge@open-net.ch
#
#  Copyright (c) 2014 Open-Net Ltd. All rights reserved.
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

from openerp.osv import fields,osv
from openerp.tools.translate import _

class project_issue(osv.osv):
    _inherit = 'project.issue'
    
    def create(self, cr, uid, vals, context=None):
        """
        Overload the original create methode to 
        add the ID of issue on its name
        """
        issue_ids = super(project_issue, self).create(
            cr, uid, vals, context=context)

        for issue in self.browse(cr, uid, issue_ids):
            prefix = "[%s] " % issue.id
            if not prefix in issue.name:
                new_name = prefix + issue.name
                self.write(cr, uid, issue.id,
                           {'name': new_name})

        return issue_ids

project_issue()
