# -*- coding: utf-8 -*-
#
#  File: models/mail_message.py
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

import logging
_logger = logging.getLogger(__name__)

class mail_message(osv.Model):
    _inherit = 'mail.message'

    # ---------- Fields management
    
    _columns = {
        'partner_cc_ids': fields.many2many('res.partner', 'mail_notification_cc', 'message_id', 'partner_id', 'CC', 
                help='Partners that have a notification pushing this message in their mailboxes'),
        'partner_cci_ids': fields.many2many('res.partner', 'mail_notification_cci', 'message_id', 'partner_id', 'CCi', 
                help='Partners that have a notification pushing this message in their mailboxes'),
    }
