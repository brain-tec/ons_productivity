# -*- coding: utf-8 -*-
# © 2018 Cousinet Eloi (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import datetime
from datetime import timedelta  

import logging
_logger = logging.getLogger(__name__)

class Followup(models.Model):
    _name = "followup.followup"
    _description = "Account Follow-up"

    ##########
    # Fields #
    ##########
    name = fields.Char(
        string='Name',
        related='company_id.name',
        readonly='True'
    )

    company_id = fields.Many2one(
        'res.company',
        'Company', 
        required='True',
        default=lambda self: self.env['res.company']._company_default_get('followup.followup')
    )

    followup_line = fields.One2many(
        'followup.followup_line',
        'followup_id', 
        string='Follow-up'
    )

class FollowupLine(models.Model):
    _name = "followup.followup_line"
    _description = "Follow-up criteria"
    _order = 'delay'

    ##########
    # Fields #
    ##########
    name = fields.Char(
        string='Follow-up Action',
        required='True'
    )

    sequence = fields.Integer(
        string='Sequence',
        help="Gives the sequence order when displaying a list of follow-ups lines."
    )

    delay = fields.Integer(
        string='Due days',
        help="The number of days after the due date of the invoice to wait before sending the reminder.  Could be negative if you want to send a polite alert beforehand.",
        required=True
    )

    followup_id = fields.Many2one(
        'followup.followup',
        string='Follow-up',
        required=True,
        ondelete='cascade'
    )
    
    description = fields.Text(
        string='Printed Message',
        translate=True,
        default="""
Exception made if there was a mistake of ours, it seems that the following amount stays unpaid. Please, take appropriate measures in order to carry out this payment in the next 8 days.
Would your payment have been carried out after this mail was sent, please ignore this message. Do not hesitate to contact our accounting department.
Best Regards,
        """
    )

    action = fields.Selection([
        ('email', 'Send an email'),
        ('letter', 'Send a letter'),
        ('manual', 'Manual action')
    ])

    manual_action_note = fields.Text(
        string='Action To Do',
        placeholder="e.g. Give a phone call, check with others, ..."
    )

    manual_action_responsible_id = fields.Many2one(
        'res.users',
        string="Assign a responsible",
        ondelete='set null'
    )

    email_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        ondelete='set null',
    ) 

    @api.model
    def create(self, values):
        rec = super(FollowupLine, self).create(values)
        for record in self.env['account.move.line'].search([
            ('full_reconcile_id', '=', False), ('account_id.deprecated', '=', False), ('account_id.internal_type', '=', 'receivable'), ('amount_residual', '>', 0)    
        ]):
            record._compute_next_follow_line_id()  
        return rec

    @api.multi
    def write(self, values):
        rec = super(FollowupLine, self).write(values)
        for record in self.env['account.move.line'].search([
            ('full_reconcile_id', '=', False), ('account_id.deprecated', '=', False), ('account_id.internal_type', '=', 'receivable'), ('amount_residual', '>', 0)    
        ]):
            record._compute_next_follow_line_id()
        return rec

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    ##########
    # Fields #
    ##########
    follow_line_id = fields.Many2one(
        'followup.followup_line',
        string='Follow-up Level',
        ondelete='restrict'
    )

    follow_date = fields.Datetime(
        string='Latest Follow-up'
    )

    amount_total = fields.Monetary(
        related="invoice_id.amount_total",
        readonly=True
    )

    residual = fields.Monetary(
        related="invoice_id.residual",
        readonly=True
    )

    ####################
    # Computed methods #
    ####################
    @api.model
    def _default_next_follow_line_id(self):
        return self.env['followup.followup_line'].search([], limit=1, order='delay asc')

    @api.depends('follow_line_id', 'date_maturity')
    def _compute_next_follow_line_id(self):
        for account_move_line in self.env['account.move.line'].search([
            ('id', 'in', list(map(lambda x: x.id, self))),
            ('full_reconcile_id', '=', False), ('account_id.deprecated', '=', False), ('account_id.internal_type', '=', 'receivable'), ('amount_residual', '>', 0)
        ]):
            if account_move_line.follow_line_id:
                account_move_line.next_follow_line_id = self.env['followup.followup_line'].search([
                    ('delay', '>', account_move_line.follow_line_id.delay)],
                    limit=1,
                    order='delay asc'
                )
                if not account_move_line.next_follow_line_id:
                    account_move_line.next_follow_line_id = self.env['followup.followup_line'].search([], limit=1, order='delay desc')
            else:
                account_move_line.next_follow_line_id = self.env['followup.followup_line'].search([], limit=1, order='delay asc')
        

    @api.depends('next_follow_line_id')
    def _compute_next_followup_date(self):
        for account_move_line in self:
            date = datetime.strptime(account_move_line.date_maturity, '%Y-%m-%d')
            date = date + timedelta(days=account_move_line.next_follow_line_id.delay)
            account_move_line.next_followup_date = date

    @api.multi
    def _compute_day_late(self):
        for account_move_line in self:
            delta = datetime.today() - datetime.strptime(account_move_line.date_maturity, '%Y-%m-%d')
            account_move_line.day_late = delta.days

    ############
    # Computed #
    ############
    next_followup_date = fields.Datetime(
        compute=_compute_next_followup_date,
        default=False,
        store=True
    )

    next_follow_line_id = fields.Many2one(
        'followup.followup_line',
        # default=_default_next_follow_line_id,
        compute=_compute_next_follow_line_id,
        store=True
    )

    day_late = fields.Integer(
        compute=_compute_day_late,
        store=False
    )

    @api.multi
    def write(self, values):
        for key in values.keys():
            if key not in ['follow_line_id', 'next_follow_line_id', 'follow_date', 'install_mode_data']:
                return super(AccountMoveLine, self).write(values)
        return super(AccountMoveLine, self.with_context(bypass_date_verif=True)).write(values)

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def _check_lock_date(self):
        if self._context.get('bypass_date_verif'):
            return True

        return super(AccountMove, self)._check_lock_date()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _get_account_move_line_letter(self):
        lines =  self.env['account.move.line'].search(
            [('partner_id', '=', self.id),
            ('next_follow_line_id.action', 'in', ['letter', 'manual']),
            ('id', 'in', self._context.get('active_ids', [])),
            ('blocked', '=', False)],
            order="next_followup_date asc"
        )
        self.account_move_line_letter_id = lines
        return lines
        
    ###################
    # Computed fields #
    ###################
    
    account_move_line_letter_id = fields.One2many(
        'account.move.line',
        compute=_get_account_move_line_letter,
        store=False
    )
