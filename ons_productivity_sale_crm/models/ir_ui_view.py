# -*- coding: utf-8 -*-
#
# File: model/ir_ui_view.py
# Module: ons_productivity_sale_crm
#
# Created by cyp@open-net.ch
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection([
            ('tree','Tree'),
            ('form','Form'),
            ('graph', 'Graph'),
            ('pivot', 'Pivot'),
            ('calendar', 'Calendar'),
            ('diagram','Diagram'),
            ('gantt', 'Gantt'),
            ('kanban', 'Kanban'),
            ('sales_team_dashboard', 'Sales Team Dashboard'),
            ('onsp_sales_crm_dashboard', 'Sales CRM Dashboard'),
            ('search','Search'),
            ('qweb', 'QWeb')], string='View Type')
