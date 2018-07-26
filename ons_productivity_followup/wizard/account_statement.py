# -*- coding: utf-8 -*-
# © 2018 Cousinet Eloi (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime
import base64

import logging
_logger = logging.getLogger(__name__)

class PrintAccountStatement(models.TransientModel):
    _name = 'followup.print.account.statement'
    _description = 'Print account statement'

    @api.multi
    def _get_selected_account_move_line(self):
        selected_account_move_line = self.env['account.move.line'].browse(
            self._context.get('active_ids', [])
        )

        return selected_account_move_line

    @api.multi
    def _get_selected_partner_id(self):
        partner_id = self.env['res.partner'].browse(
            list(set(map(lambda x: x.partner_id.id, self._get_selected_account_move_line())))
        )

        return partner_id

    selected_account_move_line = fields.One2many(
        'account.move.line',
        default=_get_selected_account_move_line,
        store=False
    )

    selected_partner = fields.One2many(
        'res.partner',
        compute=_get_selected_partner_id,
        default=_get_selected_partner_id
    )

    @api.multi
    def print_account_statement(self):
        lines = self._get_selected_account_move_line()
        pdf = self.env.ref('ons_productivity_followup.action_report_account_statement').sudo().report_action(lines)

        return pdf