# -*- coding: utf-8 -*-
#
#  File: wizards/mail_compose_message.py
#  Module: email_cc_bcc
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
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

from openerp.osv import osv, fields
from email.utils import formataddr

import logging
_logger = logging.getLogger(__name__)

class mail_compose_message(osv.TransientModel):
    _inherit = 'mail.compose.message'

    # ---------- Fields management
    
    _columns = {
        'partner_cc_ids': fields.many2many('res.partner', 'mail_compose_message_res_partner_cc_rel', 'wizard_id', 'partner_cc_id', 'CC'),
    }

    _defaults = {
         'partner_cc_ids': lambda *a: [],
    }
    
    # ---------- Content management

    def default_get(self, cr, uid, fields, context=None):
        """ Override to pre-fill the CC field """
        if context is None:
            context = {}
        res = super(mail_compose_message, self).default_get(cr, uid, fields, context=context)

        if context.get('active_model', False) and context.get('active_id', False) and res.get('partner_ids', []):
            row = self.pool.get(context['active_model']).read(cr, uid, context['active_id'], ['message_follower_ids'], context=context)
            if row and row.get('message_follower_ids', []):
                res['partner_cc_ids'] = [(6,0,[x for x in row['message_follower_ids'] if x not in res['partner_ids']])]

        return res

    def send_mail(self, cr, uid, ids, context=None):
        """
            Sends the message twice when not in mass_mail mode, so that
            its attached to the object AND it is sent as an email
        """
        ret = super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)
        
        # Call the parent function a second time if we are not in mass_mail mode,
        #   so that not only an internal message has been generated, but also mails
        for wizard in self.browse(cr, uid, ids, context=context):
            if wizard.composition_mode != 'mass_mail':
                wizard.write({'composition_mode': 'mass_mail'})
                super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)
        
        return ret
 
    def get_mail_values(self, cr, uid, wizard, res_ids, context=None):
        """
            Setup the CC field for each case
        """
        values = super(mail_compose_message, self).get_mail_values(cr, uid, wizard, res_ids, context=context)

        if wizard and wizard.partner_cc_ids:
            cc_ids = [(6,0,[partner.id for partner in wizard.partner_cc_ids])]
            cc_lst = [formataddr((partner.name, partner.email)) for partner in wizard.partner_cc_ids]
            cc_value = ','.join(cc_lst)
            for res_id in res_ids:
                values[res_id].update({
                    'partner_cc_ids': cc_ids,
                    'email_cc': cc_value,
                })

        return values

