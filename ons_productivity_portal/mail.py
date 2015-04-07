# -*- coding: utf-8 -*-
#
#  File: mail.py
#  Module: ons_productivity_portal
#
#  Created by sge@open-net.ch
#
#  Copyright (c) 2015 Open-Net Ltd. All rights reserved.
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

from openerp import netsvc
from openerp.osv import osv

# import logging
# _logger = logging.getLogger(__name__)


class mail_mail(osv.Model):
    """ Update of mail_mail class, to remove the signin URL to notifications. """
    _inherit = 'mail.mail'

    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
        """
        Return an empty string as signin
        """
        return ""
