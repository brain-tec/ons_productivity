# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import http
from openerp.addons.website_portal.controllers.main import website_account
from openerp.http import request


class WebsiteAccount(website_account):
    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def account(self):
        response = super(WebsiteAccount, self).account()
        user = request.env.user
        if user.partner_id.parent_id : 
            partner_id = user.partner_id.parent_id.id
        else: 
            partner_id = user.partner_id.id
        project_tasks = request.env['project.task'].sudo().search([
            ('project_id.partner_id', '=', partner_id),
            ('stage_id.fold', '!=', True)
        ])
        response.qcontext.update({'tasks': project_tasks})
        return response