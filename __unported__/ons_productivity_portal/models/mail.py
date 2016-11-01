# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


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
