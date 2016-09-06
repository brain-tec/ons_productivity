# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import psycopg2
import base64

from openerp import models, fields, api, _
from openerp import tools

import logging
_logger = logging.getLogger(__name__)

class mail_template(models.Model):
    _inherit = 'mail.template'

    ons_bcc = fields.Char(string='Bcc')

class mail_message(models.Model):
    _inherit = 'mail.message'

    ons_bcc = fields.Char(string='Bcc')

class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    ons_bcc = fields.Char(string="Bcc")

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        fields =  ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'ons_bcc', 'reply_to', 'attachment_ids', 'mail_server_id']
        res = super(mail_compose_message, self).generate_email_for_composer(template_id, res_ids, fields)
        return res

    # @api.model
    # def get_record_data(self, values):
    #     res = super(mail_compose_message, self).get_record_data(values)
    #     if values.get('template_id'):
    #         template = self.env['mail.template'].browse(values.get('template_id'))
    #         res['ons_bcc'] = template.ons_bcc
    #         _logger.info(template.ons_bcc)
        
    #     return res

    # @api.multi
    # def onchange_template_id(self, template_id, composition_mode, model, res_id):
       
    #     res = super(mail_compose_message, self).onchange_template_id(template_id, composition_mode, model, res_id)
    #     return res


    @api.multi
    def get_mail_values(self, res_ids):
        res = super(mail_compose_message, self).get_mail_values(res_ids)
        for res_id in res_ids:
            if res.get(res_id):
                res[res_id].update({'ons_bcc': self.ons_bcc})
        return res

class mail_mail(models.Model):
    _inherit = 'mail.mail'

    ons_bcc = fields.Char(string="Bcc")

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.
            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param bool raise_exception: whether to raise an exception if the
                email sending process has failed
            :return: True
        """
        IrMailServer = self.env['ir.mail_server']

        for mail in self:
            try:
                # TDE note: remove me when model_id field is present on mail.message - done here to avoid doing it multiple times in the sub method
                if mail.model:
                    model = self.env['ir.model'].sudo().search([('model', '=', mail.model)])[0]
                else:
                    model = None
                if model:
                    mail = mail.with_context(model_name=model.name)

                # load attachment binary data with a separate read(), as prefetching all
                # `datas` (binary field) could bloat the browse cache, triggerring
                # soft/hard mem limits with temporary data.
                attachments = [(a['datas_fname'], base64.b64decode(a['datas']))
                               for a in mail.attachment_ids.sudo().read(['datas_fname', 'datas'])]

                # specific behavior to customize the send email for notified partners
                email_list = []
                if mail.email_to:
                    email_list.append(mail.send_get_email_dict())
                for partner in mail.recipient_ids:
                    email_list.append(mail.send_get_email_dict(partner=partner))
                # headers
                headers = {}
                bounce_alias = self.env['ir.config_parameter'].get_param("mail.bounce.alias")
                catchall_domain = self.env['ir.config_parameter'].get_param("mail.catchall.domain")
                if bounce_alias and catchall_domain:
                    if mail.model and mail.res_id:
                        headers['Return-Path'] = '%s-%d-%s-%d@%s' % (bounce_alias, mail.id, mail.model, mail.res_id, catchall_domain)
                    else:
                        headers['Return-Path'] = '%s-%d@%s' % (bounce_alias, mail.id, catchall_domain)
                if mail.headers:
                    try:
                        headers.update(eval(mail.headers))
                    except Exception:
                        pass

                # Writing on the mail object may fail (e.g. lock on user) which
                # would trigger a rollback *after* actually sending the email.
                # To avoid sending twice the same email, provoke the failure earlier
                mail.write({
                    'state': 'exception',
                    'failure_reason': _('Error without exception. Probably due do sending an email without computed recipients.'),
                })
                mail_sent = False
                _logger.info(mail.ons_bcc)
                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                for email in email_list:
                    msg = IrMailServer.build_email(
                        email_from=mail.email_from,
                        email_to=email.get('email_to'),
                        subject=mail.subject,
                        body=email.get('body'),
                        body_alternative=email.get('body_alternative'),
                        email_cc=tools.email_split(mail.email_cc),
                        email_bcc=tools.email_split(mail.ons_bcc),
                        reply_to=mail.reply_to,
                        attachments=attachments,
                        message_id=mail.message_id,
                        references=mail.references,
                        object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                        subtype='html',
                        subtype_alternative='plain',
                        headers=headers)
                    try:
                        res = IrMailServer.send_email(msg, mail_server_id=mail.mail_server_id.id)
                    except AssertionError as error:
                        if error.message == IrMailServer.NO_VALID_RECIPIENT:
                            # No valid recipient found for this particular
                            # mail item -> ignore error to avoid blocking
                            # delivery to next recipients, if any. If this is
                            # the only recipient, the mail will show as failed.
                            _logger.info("Ignoring invalid recipients for mail.mail %s: %s",
                                         mail.message_id, email.get('email_to'))
                        else:
                            raise
                if res:
                    mail.write({'state': 'sent', 'message_id': res, 'failure_reason': False})
                    mail_sent = True

                # /!\ can't use mail.state here, as mail.refresh() will cause an error
                # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                if mail_sent:
                    _logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
                mail._postprocess_sent_message_v9(mail_sent=mail_sent)
            except MemoryError:
                # prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
                # instead of marking the mail as failed
                _logger.exception(
                    'MemoryError while processing mail with ID %r and Msg-Id %r. Consider raising the --limit-memory-hard startup option',
                    mail.id, mail.message_id)
                raise
            except psycopg2.Error:
                # If an error with the database occurs, chances are that the cursor is unusable.
                # This will lead to an `psycopg2.InternalError` being raised when trying to write
                # `state`, shadowing the original exception and forbid a retry on concurrent
                # update. Let's bubble it.
                raise
            except Exception as e:
                failure_reason = tools.ustr(e)
                _logger.exception('failed sending mail (id: %s) due to %s', mail.id, failure_reason)
                mail.write({'state': 'exception', 'failure_reason': failure_reason})
                mail._postprocess_sent_message_v9(mail_sent=False)
                if raise_exception:
                    if isinstance(e, AssertionError):
                        # get the args of the original error, wrap into a value and throw a MailDeliveryException
                        # that is an except_orm, with name and value as arguments
                        value = '. '.join(e.args)
                        raise MailDeliveryException(_("Mail Delivery Failed"), value)
                    raise

            if auto_commit is True:
                self._cr.commit()
        return True

class mail_thread(models.Model):
    _inherit = 'mail.thread'

    @api.multi
    def message_get_email_values(self, notif_mail=None):
        res = super(mail_thread, self).message_get_email_values(notif_mail)
        res['ons_bcc'] = notif_mail.ons_bcc
        return res