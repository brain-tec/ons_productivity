# -*- coding: utf-8 -*-
# © 2018 Cousinet Eloi (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
import base64

import logging
_logger = logging.getLogger(__name__)

class PrintFollowup(models.TransientModel):
    _name = 'followup.print.followup'
    _description = 'Print Follow-up'

    def _get_lines(self):
        lines = self.env['account.move.line'].search([
            ('next_follow_line_id.action', 'like', 'email'), 
            ('id', 'in', self._context.get('active_ids', [])),
            ('blocked', '=', False),('date_maturity','<',datetime.today()),
        ])
        return lines

    def _get_lines_letter(self):
        lines = self.env['account.move.line'].search([
            ('next_follow_line_id.action', 'in', ['letter', 'manual']),
            ('id', 'in', self._context.get('active_ids', [])),
            ('blocked', '=', False),('date_maturity','<',datetime.today()),

        ])
        return lines

    def _get_partner_without_email(self):
        lines = self._get_lines()
        partner_without_email_id = list(map(lambda x: x.partner_id.id, lines))
        partner_without_email = self.env['res.partner'].search([
            ('id', 'in', partner_without_email_id), ('email', '=', False)
        ])
        return partner_without_email

    def _is_partner_without_email(self):
        return len(self._get_partner_without_email()) > 0

    lines = fields.One2many(
        'account.move.line',
        default=_get_lines,
        store=False,
    )

    lines_letter = fields.One2many(
        'account.move.line',
        default=_get_lines_letter,
        store=False,
    )

    is_partner_without_email = fields.Boolean(
        default=_is_partner_without_email,
        store=True
    )

    partner_without_email = fields.One2many(
        'res.partner',
        compute=_get_partner_without_email,
        default=_get_partner_without_email
    )

    step = fields.Integer(
        default=1,
        store=True
    )

    @api.multi
    def print_letter(self):
        lines = self._get_lines_letter()
        pdf = self.env.ref('ons_productivity_followup.action_report_followup_letter_last_lvl').sudo().report_action(lines)
        for line in lines:
            line.write({
                'follow_date': datetime.now(),
                'follow_line_id': line.next_follow_line_id.id
            })

        return pdf

    @api.multi
    def send_email(self):
        lines = self._get_lines()

        lines_grouped_by_partner = {}
        for line in lines:
            if line.partner_id in lines_grouped_by_partner:
                lines_grouped_by_partner[line.partner_id].append(line)
            else:
                lines_grouped_by_partner[line.partner_id] = [line]

        for partner, partner_lines in lines_grouped_by_partner.items():
            lines = list(set(map(lambda x: x.id, partner_lines)))

            pdf, data = self.env.ref('ons_productivity_followup.action_report_followup_letter').sudo().render(lines)
            attachment = self.env['ir.attachment'].create({
                'name': line.invoice_id.display_name or line.invoice_id.name or 'rappel.pdf',
                'type': 'binary',
                'datas': base64.encodestring(pdf),
                'datas_fname': "rappel.pdf",
                'res_model': 'account.invoice',
                'res_id': line.invoice_id.id,
                'mimetype': 'application/x-pdf'
            })
            attachment_ids = [attachment.id]
            email_template = partner_lines[0].next_follow_line_id.email_template_id
            values = email_template.generate_email(partner.id)
            if not email_template:
                raise UserError(_('The followup line need to be related to a template id'))

            values['attachment_ids'] = [(4, attachment_ids[0])]
            if len(partner_lines) > 0 and partner_lines[0].invoice_id and partner_lines[0].invoice_id.partner_id:
                values['email_to'] = partner_lines[0].invoice_id.partner_id.email
            else:
                values['email_to'] = partner.email
            
            if values['email_to']:
                mail = self.env['mail.mail']
                mail.send(mail.create(values))
                for line in partner_lines:
                    line.write({
                        'follow_date': datetime.now(),
                        'follow_line_id': line.next_follow_line_id.id
                    })


