# -*- coding: utf-8 -*-
#
#  File: ons_productivity_stats.py
#  Module: ons_productivity_stats
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
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

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
from datetime import *
from dateutil.relativedelta import relativedelta
import base64
import netsvc
import tools

logger = netsvc.Logger()

class stats_base(osv.osv):
    _name = 'ons.stats'
    _description = 'Statistics'

    # ------------ Fields management

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'company_id': fields.many2one('res.company', 'Company'),
        'comp_currency_id': fields.related('company_id', 'currency_id', relation='res.currency', type='many2one', string='Compagny currency', store=False),
        'currency_ids': fields.many2many('res.currency', 'ons_stats_to_currencies', 'stats_id', 'currency_id', 'Compl. currencies'),
        'date_from': fields.date('From'),
        'date_to': fields.date('To'),
        'is_template': fields.boolean('Template?'),
        'base_filename': fields.char('Base file name', size=60),
        'report_sent': fields.boolean('Report sent'),
        'void': fields.char('Void', size=1),
    }
    
    _defaults = {
        'company_id': lambda s,c,u,ct: s.pool.get('res.users').browse(c,u,u,context=ct).company_id.id,
        'comp_currency_id': lambda s,c,u,ct: s.pool.get('res.users').browse(c,u,u,context=ct).company_id.currency_id.id,
        'is_template': lambda *a: True,
        'void': lambda *a: ' ',
    }

stats_base()

class stats_user_line_base(osv.osv):
    _name = 'ons.stats_user_line'
    _description = 'Statistic user line'

    # ------------ Fields management

    _columns = {
        'name': fields.many2one('res.users', 'Salesperson', required=True),
        'stats_id': fields.many2one('ons.stats', 'Statistics', required=True),
        'is_template': fields.boolean(string='Template?'),
    }
    
    _defaults = {
        'is_template': lambda *a: True,
    }

stats_user_line_base()

class stats_currency_line(osv.osv):
    _name = 'ons.stats_currency_line'
    _description = 'Statistic currency line'

    # ------------ Fields management

    _columns = {
        'name': fields.many2one('res.currency', 'Currency', required=True),
        'stats_id': fields.many2one('ons.stats', 'Statistics', required=True),
        'user_line_id': fields.many2one('ons.stats_user_line', 'Salesperson', required=True),
        'user_id': fields.related('stat_user_line_id', 'user_id', type='many2one', relation='res.users', string='Salesperson', store=False),
        'sale_stat': fields.float('Sales', digits_compute=dp.get_precision('Account')),
        #'draft_inv_stat': fields.float('Draft invoices', digits_compute=dp.get_precision('Account')),
        'opened_inv_stat': fields.float('Invoices', digits_compute=dp.get_precision('Account')),
    }

stats_currency_line()

class stats_stats_curr_line(osv.osv):
    _name = 'ons.stats_stats_curr_line'
    _description = 'Statistic curr. line'

    # ------------ Fields management

    _columns = {
        'name': fields.many2one('ons.stats', 'Statistics', required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', required=True),
        'sale_stat': fields.float('Sales', digits_compute=dp.get_precision('Account')),
        #'draft_inv_stat': fields.float('Draft invoices', digits_compute=dp.get_precision('Account')),
        'opened_inv_stat': fields.float('Invoices', digits_compute=dp.get_precision('Account')),
        'void': fields.char('Void', size=1),
    }

    _defaults = {
        'void': lambda *a: ' ',
    }

stats_stats_curr_line()

class stats_user_line(osv.osv):
    _inherit = 'ons.stats_user_line'

    # ------------ Fields management

    _columns = {
        'currency_line_ids': fields.one2many('ons.stats_currency_line', 'user_line_id', 'Currency statistics'),
    }

    # ------------ Utilities

    def compute_stats(self, cr, uid, stats, user_line, context=None):
        if not stats or not user_line: return False
        
        curr_line_obj = self.pool.get('ons.stats_currency_line')
        sale_obj = self.pool.get('sale.order')
        invoice_obj = self.pool.get('account.invoice')
        currency_obj = self.pool.get('res.currency')
        main_stat_obj = self.pool.get('ons.stats_stats_curr_line')
        
        # Remove the old stuff
        todo = [x.id for x in user_line.currency_line_ids]
        if todo:
            curr_line_obj.unlink(cr, uid, todo, context=context)
        todo = [x.id for x in stats.main_line_ids]
        if todo:
            self.pool.get('ons.stats_stats_curr_line').unlink(cr, uid, todo, context=context)
        
        currency_ids = [stats.comp_currency_id.id] + [x.id for x in stats.currency_ids]
        for currency_id in currency_ids:
            tot_sale = 0.0
            tot_draft_inv = 0.0
            tot_opened_inv = 0.0
            main_stat_id = main_stat_obj.search(cr, uid,  [('name','=', stats.id),('currency_id','=',currency_id)], context=context)
            if main_stat_id:
                main_stat_id = main_stat_id[0]
                main_stat = main_stat_obj.browse(cr, uid, main_stat_id, context=context)
                if main_stat:
                    tot_sale = main_stat.sale_stat
                    #tot_draft_inv = main_stat.draft_inv_stat
                    tot_opened_inv = main_stat.opened_inv_stat
                else:
                    main_stat_id = False

            # Prepare a new user currency stats line
            vals = {
                'name': currency_id,
                'user_line_id': user_line.id,
                'sale_stat': 0.0,
                #'draft_inv_stat': 0.0,
                'opened_inv_stat': 0.0,
                'stats_id': stats.id,
            }
            
            # Compute the sales (without taxes)
            filters = [
                ('user_id', '=', user_line.name.id),
                ('date_order','>=', stats.date_from),
                ('date_order','<=', stats.date_to),
                ('state','in',['waiting_date','manual','progress','shipping_except','invoice_except','done']),
                ('stats_id','=', None)
            ]
            todo = []
            total = 0
            so_ids = sale_obj.search(cr, uid, filters, context=context)
            logger.notifyChannel(' ***** Stats', netsvc.LOG_INFO, " SO list:" + str(so_ids))
            if so_ids:
                for so in sale_obj.browse(cr, uid, so_ids, context=context):
                    amount = so.amount_untaxed
                    if so.pricelist_id.currency_id.id != currency_id:
                        continue
                    total += amount
                    todo += [str(so.id)]
            vals['sale_stat'] = total
            tot_sale += total
            if todo:
                q = "Update sale_order set stats_id=" + str(stats.id) + " where id in (%s)" % ','.join(todo)
                cr.execute(q)
            
            # Compute the opened and closed invoices (without taxes)
            filters = [
                ('user_id', '=', user_line.name.id),
                ('date_invoice','>=', stats.date_from),
                ('date_invoice','<=', stats.date_to),
                ('type','in',['out_invoice','out_refund']), 
                ('state','in',['open','paid']), 
                ('stats_id','=', None)
            ]
            todo = []
            total = 0
            inv_ids = invoice_obj.search(cr, uid, filters, context=context)
            logger.notifyChannel(' ***** Stats', netsvc.LOG_INFO, " INV list:" + str(inv_ids))
            if inv_ids:
                for inv in invoice_obj.browse(cr, uid, inv_ids, context=context):
                    amount = inv.amount_untaxed
                    if inv.currency_id.id != currency_id:
                        continue
                    if inv.type == 'out_invoice':
                        total += amount
                    else:
                        total -= amount
                    todo += [str(inv.id)]
            vals['opened_inv_stat'] = total
            tot_opened_inv += total
            if todo:
                q = "Update account_invoice set stats_id=" + str(stats.id) + " where id in (%s)" % ','.join(todo)
                cr.execute(q)

            new_line_id = curr_line_obj.create(cr, uid, vals, context=context)

            vals = {
                'sale_stat': tot_sale,
                #'draft_inv_stat': tot_draft_inv,
                'opened_inv_stat': tot_opened_inv,
            }
            if main_stat_id:
                main_stat_obj.write(cr, uid, [main_stat_id], vals, context=context)
            else:
                vals.update({
                    'name': stats.id,
                    'currency_id': currency_id,
                })
                main_stat_id = main_stat_obj.create(cr, uid, vals, context=context)

stats_user_line()

class stats1(osv.osv):
    _inherit = 'ons.stats'

    # ------------ Fields management

    _columns = {
        'user_line_ids': fields.one2many('ons.stats_user_line', 'stats_id', 'Salesperson statistics'),
        'main_line_ids': fields.one2many('ons.stats_stats_curr_line', 'name', 'Period statistics'),
    }

stats1()

class sale_order(osv.osv):
    _inherit = 'sale.order'

    # ------------ Fields management

    _columns = {
        'stats_id': fields.many2one('ons.stats', 'Statistics', readonly=True),
        'currency_id': fields.related('pricelist_id','currency_id', relation='res.currency', type='many2one', string='Currency', readonly=True),
    }

sale_order()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    # ------------ Fields management

    _columns = {
        'stats_id': fields.many2one('ons.stats', 'Statistics', readonly=True),
    }

account_invoice()

class stats2(osv.osv):
    _inherit = 'ons.stats'

    # ------------ Fields management

    def _ons_count_stats(self, cr, uid, ids, field_names, arg=None, context=None):
    
        so_obj = self.pool.get('sale.order')
        inv_obj = self.pool.get('account.invoice')
    
        ret = {}
        for id in ids:
            l_so = so_obj.search(cr, uid, [('stats_id','=',id)], context=context)
            l_inv = inv_obj.search(cr, uid, [('stats_id','=',id)], context=context)
            ret[id] = {
                'sales_count': len(l_so or []),
                'invoices_count': len(l_inv or []),
            }
        
        return ret

    _columns = {
        'sale_ids': fields.one2many('sale.order', 'stats_id', 'Sales'),
        'invoice_ids': fields.one2many('account.invoice', 'stats_id', 'Invoices'),
        'sales_count': fields.function(_ons_count_stats, method=True, type='integer', string='Sales nb.', multi='sales_count'),
        'invoices_count': fields.function(_ons_count_stats, method=True, type='integer', string='Invoices Nb.', multi='invoices_count'),
    }

    # ------------ Instances management

    def unlink(self, cr, uid, ids, context=None):
        
        curr_todo = []
        user_todo = []
        main_todo = []
        for stat in self.browse(cr, uid, ids, context=context):
            for user_line in stat.user_line_ids:
                user_todo += [user_line.id]
                
                for curr_line in user_line.currency_line_ids:
                    curr_todo += [curr_line.id]

            main_todo += [x.id for x in stat.main_line_ids]
        
        if curr_todo:
            self.pool.get('ons.stats_currency_line').unlink(cr, uid, curr_todo, context=context)
        if user_todo:
            self.pool.get('ons.stats_user_line').unlink(cr, uid, user_todo, context=context)
        if main_todo:
            self.pool.get('ons.stats_stats_curr_line').unlink(cr, uid, main_todo, context=context)
        
        return super(stats2, self).unlink(cr, uid, ids, context=context)
    
    def create(self, cr, uid, values, context={}):
        if 'report_sent' not in values:
            values['report_sent'] = False
        
        return super(stats2, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context={}):
        if 'report_sent' not in values:
            values['report_sent'] = False
        
        return super(stats2, self).write(cr, uid, ids, values, context=context)

    # ------------ User interface related

    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        return super(stats2, self).fields_view_get(cr, user, view_id=view_id, view_type=view_type, context=context, toolbar=False, submenu=submenu)

    # ------------ Utilities
    
    def wiz_generate(self, cr, uid, ids, context=None):
        return True
    
    def do_generate(self, cr, uid, template, date_from, date_to, context=None):
        if not template or not date_from or not date_to: return False
        logger.notifyChannel(' ***** Stats', netsvc.LOG_INFO, "Generating the report '%s' with date_from=%s date_to=%s" % (template, str(date_from), str(date_to) ) )
        
        if template:
            if isinstance(template, (int,long)):
                template = self.browse(cr, uid, template, context=context)
            elif isinstance(template,(type(''),type(u''))):
                template = self.search(cr, uid, [('name','=',template)], context=context)
                if template:
                    template = self.browse(cr, uid, template[0], context=context)
        if not template:
            return False
        
        user_line_obj = self.pool.get('ons.stats_user_line')
        
        # Prepare a new report from the template
        default = {
            'is_template': False,
            'date_from': date_from,
            'date_to': date_to,
        }
        new_id = self.copy(cr, uid, template.id, default=default, context=context)
        stats = self.browse(cr, uid, new_id, context=context)
        
        # Compute the stats of each linked user
        for user_line in stats.user_line_ids:
            user_line.write({'is_template':False})
            ret = user_line_obj.compute_stats(cr, uid, stats, user_line, context=context)
        
        return new_id

    # ------------ Scheduler

    def generate_report(self, cr, uid, template, days_before_start, days_before_end, context=None):
        logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Generating the report: '%s' from %s to %s, context is %s" % (template, days_before_start, days_before_end, str(context)))

        # Compute the interval
        date_from = (datetime.now() + relativedelta(days=days_before_start or 0.0)).strftime('%Y-%m-%d')
        date_to   = (datetime.now() + relativedelta(days=days_before_end   or 0.0)).strftime('%Y-%m-%d')

        # Build the report
        report_id = self.do_generate(cr, uid, template, date_from, date_to, context=context)
        if not report_id:
            logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "No stats generated")
            return False
        
        #self.write(cr, uid, [report_id], {'base_filename': file_name}, context=context)
        logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Report generated, id=%d" % report_id )

        return True

    def send_reports(self, cr, uid, send_to, email_from, context=None):
        logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Sending the unsent reports to %s, context is %s" % (str(send_to), str(context)))
        if not email_from or not send_to:
            logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Check configuration: send_to should be a list of emails, email_from: an email" % (template, days_before_start, days_before_end, send_to))
        
        # Retrieve the unsent the reports
        stats_ids = self.search(cr, uid, [('report_sent','=',False)], context=context)
        if not stats_ids:
            logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "No stats found")
            return False

        # Print each report in a temp file
        report_name = 'rml.ons_stats'
        report_obj = self.pool.get('ir.actions.report.xml')
        report_id = report_obj.search(cr, uid, [('report_name','=',report_name)])
        if not report_id:
            logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Report not found: %s" % (report_name,))
            return False
        service = netsvc.LocalService('report.'+report_name)
        payloads = {}
        context.update({
            'project_id': False,
            'section_id': False,
            'department_id': False,
            'tz': u'Europe/Zurich',
        })
        for stats in self.browse(cr, uid, stats_ids, context=context):
            datas = {
                'id': stats.id,
                'model': 'ons_stats', 
                'report_type':'pdf',
                }
            ctx = context.copy()
            ctx.update({
                'active_id': int(stats.id),
                'active_ids': [int(stats.id)],
                'active_model': 'ons.stats',
            })
            logger.notifyChannel(' ***** Stats scheduler', netsvc.LOG_DEBUG, "Call to print with report_id=%s and datas: %s" % (str(report_id), str(datas)) )
            (result, format) = service.create(cr, uid, report_id, datas, ctx)
    
            # Prepare an email with the printed report as attachment
            subject = stats.name
            interval = str(_(u"from %s to %s") % (stats.date_from, stats.date_to))
            dafas_fname = tools.ustr(stats.name) + " - " + interval + "." + format
            payloads[dafas_fname] = base64.b64encode(result)
    
        addresses = {
            'From': email_from,
            'To':   send_to,
        }
        bodies = {
            'text': subject,
            'html': subject,
        }
        
        self.pool.get('ons_messaging.template').email_send(cr, uid, addresses, subject, bodies, payload)
        self.write(cr, uid, stats_ids, {'report_sent': True}, context=context)

        return True

stats2()
