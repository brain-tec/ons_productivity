# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def _get_tasks(self):
		tasks = []
		timesheets = []
		records = {}
		for record in self:
			for invoice_line in record.invoice_line_ids:
				for sale_line in invoice_line.sale_line_ids:
					if record.task_date_from:
						for task in sale_line.task_id:
							# records[task] = []
							if task.timesheet_ids:
								timesheets = []
								for time in task.timesheet_ids:
									if record.task_date_to:
										if time.date >= record.task_date_from and time.date <= record.task_date_to:
											if not timesheets:
												timesheets = time
											elif timesheets:
												timesheets += time
									else:
										if time.date >= record.task_date_from:
											if not timesheets:
												timesheets = time
											elif timesheets:
												timesheets += time
								if timesheets:
									records[task] = timesheets
		_logger.info(records)
		return records

	task_date_from = fields.Date(string='Date de début')
	task_date_to = fields.Date(string='Date de fin')