# -*- encoding: utf-8 -*-
#
#  File: models/soap_servers.py
#  Module: ons_productivity_soap
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013-TODAY Open-Net Ltd. All rights reserved.

from suds import WebFault
from suds.client import Client
from suds.transport import Transport
import httplib2, StringIO
from openerp.exceptions import AccessError, ValidationError, except_orm
from openerp import api, fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


import logging
_logger = logging.getLogger(__name__)


# ---- This let's you change SUDs' user agent name

class Httplib2Response:
    pass
class Httplib2Transport(Transport):

    def __init__(self, **kwargs):
        Transport.__init__(self)
        self.http = httplib2.Http()

    def send(self, request):
        url = request.url
        message = request.message
        headers = request.headers
        headers['User-Agent']='XYZ'
        response = Httplib2Response()
        response.headers, response.message = self.http.request(url,
                "PUT", body=message, headers=headers)

        return response

    def open(self, request):
        response = Httplib2Response()
        request.headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

        response.headers, response.message = self.http.request(request.url, "GET",
            body=request.message, headers=request.headers)

        return StringIO.StringIO(response.message)


class SOAPInfo(except_orm):
    def __init__(self, msg):
        super(SOAPInfo, self).__init__(msg)


class ExternalServerBase(models.Model):
    _name = 'ons.soap.external.server'
    _description = 'External Server'
                
    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    wsdl_suffix = fields.Char(string='Wsdl suffix')
    apiusername = fields.Char(string='User Name')
    apipass = fields.Char(string='Password')
    timeout = fields.Integer(string='Time-out', default=3600)
    admin_panel = fields.Char(stirng='Administration panel')
    use_alt_transport = fields.Boolean(string='Use alternate transport', default=False)
    simulation = fields.Boolean(string='Simulation', default=False,
        help='Permet de ne faire aucune mise modification sur le serveur distant')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Referential names must be unique !')
    ]
    

class FieldMappingLine(models.Model):
    _name = 'ons.soap.external.server.field_map_line'
    _description = 'Field mapping line for the external server'
    
    name = fields.Char(string='Magento field')
    field_id = fields.Many2one('ir.model.fields', string='OpenERP field',
        required=True, domain=[('model','in',['product.product','product.template'])])
    external_server_id = fields.Many2one('ons.soap.external.server', string='Server')


class LogEntry(models.Model):
    _name = 'ons.soap.external.server.log_entry'
    _description = 'Log entries for the external server'
    _order = 'external_server_id asc, id desc'

    name = fields.Char(string='Title', required=True)
    doing = fields.Char(string='Doing', default='stopped')
    log = fields.Text(string='Log entry', required=True)
    log_line = fields.Char(compute='_get_log_line', string='Log line')
    last_update = fields.Datetime(compute='_get_last_update', string='Date')
    create_date = fields.Datetime(string='Date', readonly=True)
    write_date = fields.Datetime(string='Date', readonly=True)
    external_server_id = fields.Many2one('ons.soap.external.server', string='Server', required=True, ondelete='cascade')

    @api.multi
    @api.depends('log')
    def _get_log_line(self):
        for row in self:
            l = row.log.split('\n')[0][0:100]
            if len(l) != len(row.log):
                l += '...' 
            row.log_line = l
    
    @api.multi
    @api.depends('create_date','write_date')
    def _get_last_update(self):
        for row in self:
            row.last_update = row.write_date or row.create_date


class ExternalServer(models.Model):
    _inherit = 'ons.soap.external.server'
                
    field_mapping_ids = fields.One2many('ons.soap.external.server.field_map_line', 'external_server_id', string='Fields mapping')
    logs_ids = fields.One2many('ons.soap.external.server.log_entry', 'external_server_id', string='Logs')

    @api.one
    def copy(self, default=None):
        return super(ExternalServer, self).copy({'name': self.name + _(' (Copy)')})

    @api.multi
    def connect(self):
        self.ensure_one()

        if not self:
            return (False, False)

        try:
            soap_url = str(self.location)
            wsdl_url = soap_url + (self.wsdl_suffix or '')

            http = False
            if self.use_alt_transport:
                # Define a user-agent different from Python's default one
                http = Httplib2Transport()

            client = Client(wsdl_url, location=soap_url, username=self.apiusername, password=self.apipass, timeout=self.timeout, transport=http)
            soap_server = client.service
            session_id = soap_server.login(self.apiusername, self.apipass)
            
            return (soap_server, session_id)

        except WebFault, f:
            raise AccessError(str(f.fault))
        except Exception, e:
            msg = _("Could not connect to server\nCheck location, username & password.") +'\n' + str(e)
            raise ValidationError(msg)

    @api.multi
    def action_test_connection(self):
        for row in self:
            conn, session = row.connect()

            if session:
                raise SOAPInfo("Successfull connection")
        
        return False

    @api.multi
    def action_remove_old_logs(self):
        current_date = datetime.now()
        old_date = (current_date + relativedelta(months=-6)).strftime('%Y-%m-%d')
        query = "delete from ons_soap_external_server_log_entry where create_date::text < '%s'" % (old_date,)
        self._cr.execute(query)

        return True

    def show_my_logs(self):
        model,res_id = self.env['ir.model.data'].get_object_reference('ons_productivity_soap', 'onsp_soap_srv_extern_srv2logs')
        if not model or not res_id: return False

        ret = self.env[model].read(self.env.cr, self.env.uid, res_id, context=self.env.context)
        ret.update({
            'name': self.name or '-',
            'domain': str([('external_server_id','=',self.ids and self.ids[0].id or False)]),
            'nodestroy': True
            })
        
        return ret
    
    @api.model
    def add_to_log(self, vals):
        Logs = self.env['ons.soap.external.server.log_entry']
        
        if vals.get('entry_id'):
            log_id = vals['entry_id']
            log = Logs.browse(log_id)
            if log:
                v = {}
                if vals.get('doing', ''):
                    v['doing'] = vals['doing']
                if vals.get('log', ''):
                    v['log'] = log.log+vals['log']
                if v:
                    log.write(v)

                return log
        
        if vals.get('name'):
            log = Logs.search([('name','=',vals['name'])])
            if not log:
                log = Logs.create(vals)
            else:
                v = {}
                if vals.get('doing', ''):
                    v['doing'] = vals['doing']
                if vals.get('log', ''):
                    v['log'] = log.log+vals['log']
                if v:
                    log.write(v)

            return log
    
        return False

    @api.multi
    def update_external_product(self, product, ext_prod_id, attribute_set='Default'):
        self.ensure_one()

        ext_srv_res = {
            'msg': [],
            'status': False,
        }
        if not product or not ext_prod_id:
            msg = _("External product sync says: missing product")
            ext_srv_res['msg'] += [msg]
            _logger.info(msg)

            return ext_srv_res

        prod_fields = [x.field_id.name for x in self.field_mapping_ids]
        if not prod_fields:
            msg = _("External product sync says: Nothing to sync for product %s") % str(product.display_name)
            ext_srv_res['msg'] += [msg]
            _logger.info(msg)

            return ext_srv_res

        # Now, we need a connection
        conn, session = self.connect()
        if not session:
            msg = _("External product sync says: Can't connect to the server %s") % str(self.name)
            ext_srv_res['msg'] += [msg]
            _logger.info(msg)

            return ext_srv_res

        # Retrieve the attribute set ID, if not given
        if not isinstance(attribute_set, type(1)):
            lst = conn.catalogProductAttributeSetList(session)
            for item in lst:
                if item['name'] == attribute_set:
                    attribute_set = item['set_id']
                    break
        
        # Retrieve the list of attributes of this set, so that we can handle the 'select' types
        attrs = {}
        lst = conn.catalogProductAttributeList(session, attribute_set)
        for item in lst:
            if 'type' not in item: continue
            a_vals = { 'id': item['attribute_id'], 'type': item['type'] }
            if item['type'] == 'select':
                opts = conn.catalogProductAttributeOptions(session, item['attribute_id'])
                o_vals = {}
                for opt in opts:
                    if opt['label'] is None: continue
                    o_vals[r'' + opt['label']] = opt['value']
                a_vals['opts'] = o_vals
            attrs[str(item['code'])] = a_vals

        msg = _("External product sync says: starting to sync the product %s") % str(product.display_name)
        ext_srv_res['msg'] += [msg]
        _logger.info(msg)

        # Build the list of attribute values
        # ... and add each missing option as well
        additional_attributes = []
        for map_line in self.field_mapping_ids:
            
            # Retrieve the attribute...
            attr_name = str(map_line.name)
            if attr_name not in attrs:
                msg = _("External product sync says: Cant find the attribute '%s' in the attribute set '%s' the product with ID=%s") % (attr_name, str(attribute_set), str(oe_prod_id))
                ext_srv_res['msg'] += [msg]
                _logger.info(msg)

                continue
            
            # ... and its real value (in case of a many2one field)
            try:
                attr_val = getattr(product, map_line.field_id.name)
            except:
                continue
            if hasattr(attr_val,'id'):
                attr_val = attr_val.id
            if not attr_val:
                attr_val = '' # Else we'll find the word 'False' as a result...

            # Update the Magento attribut select list if this is such a field
            if attrs[attr_name].get('type','') == 'select':
                if map_line.field_id.ttype == 'boolean':
                    res = False
                    if attr_val:
                        if len(attrs[attr_name]['opts']):
                            res = attrs[attr_name]['opts'][attrs[attr_name]['opts'].keys()[0]]
                    attr_val = res
                else:
                    if attr_val in attrs[attr_name]['opts']:
                        attr_val = attrs[attr_name]['opts'][attr_val]
                    else:
                        labels = [{
                            'store_id': ['0'],
                            'value': attr_val,
                        }]
                        option = {
                            'label': labels,
                            'order': len(attrs[attr_name]['opts'])+1,
                            'is_default': 0,
                        }
                        attr_val = conn.catalogProductAttributeAddOption(session, attrs[attr_name]['id'], option)

            # Obviously...
            additional_attributes.append({
                'key': attr_name,
                'value': attr_val,
            })

        if additional_attributes:
            msg = _("External product sync says: the values sent are: ") + str(additional_attributes)
            ext_srv_res['msg'] += [msg]
            _logger.info(msg)
            conn.catalogProductUpdate(session, ext_prod_id, {'additional_attributes':{'single_data': additional_attributes}})

        msg = _("External product sync says: end of sync")
        ext_srv_res['msg'] += [msg]
        ext_srv_res['status'] = True
        _logger.info(msg)

        return ext_srv_res

