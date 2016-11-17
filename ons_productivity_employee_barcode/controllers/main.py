
from openerp import http
from openerp.addons.web import http
from openerp.http import request

#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class WebsiteSale(http.Controller):

    @http.route(['/set_employee_barcode/<string:barcode>'], type='http')
    def set_employee_barcode(self, barcode, **post):
        _logger.info(barcode)
        request.session['employee_barcode'] = barcode

    @http.route(['/employee_barcode_logout'], type='http')
    def employee_barcode_logout(self, **post):
        request.session['employee_barcode'] = ''