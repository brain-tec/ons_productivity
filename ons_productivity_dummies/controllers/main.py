# -*- coding: utf-8 -*-

from odoo.addons.website.controllers.main import Website
from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class website_dummy(Website):

    @http.route(website=True, auth="public")
    def web_login(self, redirect=None, *args, **kw):
        res = super(website_dummy, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            redirect = '/web?' + request.httprequest.query_string
            return http.redirect_with_hash(redirect)
        return res