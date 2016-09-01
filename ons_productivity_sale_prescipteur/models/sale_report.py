# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

class sale_report(models.Model):
    _inherit = "sale.report"

    prescriteur_id = fields.Many2one('res.partner', 'Prescripteur', readonly=True)

    def _select(self):
        return super(sale_report, self)._select() + ", s.ons_prescripteur as prescriteur_id"

    def _group_by(self):
        return super(sale_report, self)._group_by() + ", s.ons_prescripteur"