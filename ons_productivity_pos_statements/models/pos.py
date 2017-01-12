# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = "pos.session"

    @api.multi
    def wkf_action_open(self):
        res = super(PosSession, self).wkf_action_open()
        for session in self:
            for statement in session.statement_ids:
                last_bnk_stmt = self.env['account.bank.statement'].search(
                    [('journal_id', '=', statement.journal_id.id),('id', '!=', statement.id)], limit=1)
                _logger.info(last_bnk_stmt)
                if last_bnk_stmt:
                    statement.balance_start = last_bnk_stmt.balance_end
                else:
                    statement.balance_start = 0
        return res