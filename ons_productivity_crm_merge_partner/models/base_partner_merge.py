# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import openerp
from openerp.osv import osv


class MergePartnerAutomatic(osv.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, cr, uid, partner_ids, dst_partner=None, context=None):
        proxy = self.pool.get('res.partner')
        child_ids = set()
        for partner_id in partner_ids:
            child_ids = child_ids.union(set(proxy.search(cr, uid, [('id', 'child_of', [partner_id])])) - set([partner_id]))
        if set(partner_ids).intersection(child_ids):
            for partner_id in proxy.browse(cr, uid, partner_ids, context):
                partner_id.parent_id = False
        super(MergePartnerAutomatic, self)._merge(cr, uid, partner_ids, dst_partner, context=context)