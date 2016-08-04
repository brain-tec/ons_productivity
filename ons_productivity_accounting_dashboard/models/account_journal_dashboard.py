# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from babel.dates import format_datetime, format_date
from openerp import fields, models, api, _
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import logging
#Get the logger
_logger = logging.getLogger(__name__)


class account_journal(models.Model):
    _inherit = 'account.journal'

    @api.multi
    def get_line_graph_datas(self):
        data = []
        today = datetime.today()
        last_month = today + timedelta(days=-90)
        bank_stmt = []
        # Query to optimize loading of data for bank statement graphs
        # Return a list containing the latest bank statement balance per day for the
        # last 30 days for current journal
        query = """SELECT a.date, a.balance_end 
                        FROM account_bank_statement AS a, 
                            (SELECT c.date, max(c.id) AS stmt_id 
                                FROM account_bank_statement AS c 
                                WHERE c.journal_id = %s 
                                    AND c.date > %s 
                                    AND c.date <= %s 
                                    GROUP BY date, id 
                                    ORDER BY date, id) AS b 
                        WHERE a.id = b.stmt_id ORDER BY a.date;"""

        self.env.cr.execute(query, (self.id, last_month, today))
        bank_stmt = self.env.cr.dictfetchall()
        for stmt in bank_stmt:
            data.append({'x': stmt.get('date'), 'y':stmt.get('balance_end'), 'name': stmt.get('date')})
        return [{'values': data, 'area': True}]

    @api.multi
    def get_bar_graph_datas(self):
        data = []
        today = datetime.strptime(fields.Date.context_today(self), DF)
        data.append({'label': _('Past'), 'value':0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang', 'en_US')))
        first_day_of_week = today + timedelta(days=-day_of_week+1)
        for i in range(-1,4):
            if i==0:
                label = _('This Week')
            elif i==3:
                label = _('Future')
            else:
                start_week = first_day_of_week + timedelta(days=i*7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' +str(end_week.day)+ ' ' + format_date(end_week, 'MMM', locale=self._context.get('lang', 'en_US'))
                else:
                    label = format_date(start_week, 'd MMM', locale=self._context.get('lang', 'en_US'))+'-'+format_date(end_week, 'd MMM', locale=self._context.get('lang', 'en_US'))
            data.append({'label':label,'value':0.0, 'type': 'past' if i<0 else 'future'})

        # Build SQL query to find amount aggregated by week
        select_sql_clause = """SELECT sum(residual_company_signed) as total, min(date_due) as aggr_date from account_invoice where journal_id = %(journal_id)s and state = 'open'"""
        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0,7):
            if i == 0:
                query += "("+select_sql_clause+" and date_due < '"+start_date.strftime(DF)+"')"
            elif i == 6:
                query += " UNION ALL ("+select_sql_clause+" and date_due >= '"+start_date.strftime(DF)+"')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL ("+select_sql_clause+" and date_due >= '"+start_date.strftime(DF)+"' and date_due < '"+next_date.strftime(DF)+"')"
                start_date = next_date

        self.env.cr.execute(query, {'journal_id':self.id})
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            if query_results[index].get('aggr_date') != None:
                data[index]['value'] = query_results[index].get('total')
        return [{'values': data}]