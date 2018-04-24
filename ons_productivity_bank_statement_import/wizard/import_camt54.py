# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import re
from lxml import etree
from odoo import models

import logging
_logger = logging.getLogger(__name__)

class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _check_camt54(self, data_file):
        try:
            root = etree.parse(io.BytesIO(data_file)).getroot()
        except:
            return None
        if root.tag.find('camt.054') != -1:
            return root
        return None

    def _parse_file(self, data_file):
        xml_root = self._check_camt54(data_file)
        if xml_root is not None:
            return self._parse_file_camt54(xml_root)
        return super(AccountBankStatementImport, self)._parse_file(data_file)

    def _parse_file_camt54(self, xml_root):
        namespaces = {k or 'xmlns': v for k, v in xml_root.nsmap.items()}
        statement = []
        account_number = xml_root[0].xpath('xmlns:Ntfctn/xmlns:Acct/xmlns:Id/xmlns:IBAN/text()', namespaces=namespaces)[0]
        currency = None

        for entry in xml_root[0].findall('xmlns:Ntfctn/xmlns:Ntry', namespaces=namespaces):
            entry_ref = entry.xpath('xmlns:NtryRef/text()', namespaces=namespaces)[0]
            entry_date = entry.xpath('xmlns:BookgDt/xmlns:Dt/text()', namespaces=namespaces)[0]
            entry_AcctSvcrRef = entry.xpath('xmlns:AcctSvcrRef/text()', namespaces=namespaces)[0]

            transactions = []

            for transaction in entry.findall('xmlns:NtryDtls/xmlns:TxDtls', namespaces=namespaces):
                ref = transaction.xpath('xmlns:RmtInf//xmlns:Ref/text()', namespaces=namespaces)[0]
                ref_type = transaction.xpath('xmlns:RmtInf//xmlns:CdOrPrtry/xmlns:Prtry/text()', namespaces=namespaces)[0]
                amount = transaction.xpath('xmlns:Amt/text()', namespaces=namespaces)[0]
                # currency = transaction.xpath('xmlns:Amt/@Ccy', namespaces=namespaces)[0]
                trans_date = transaction.xpath('xmlns:RltdDts/xmlns:AccptncDtTm/text()', namespaces=namespaces)[0].split('T')[0]
                trans_AcctSvcrRef = transaction.xpath('xmlns:Refs/xmlns:AcctSvcrRef/text()', namespaces=namespaces)[0]
                partner_name = transaction.xpath('xmlns:RltdPties/xmlns:Dbtr/xmlns:Nm/text()', namespaces=namespaces)[0]
                partner_acc_nmb = transaction.xpath('xmlns:RltdPties/xmlns:DbtrAcct/xmlns:Id/xmlns:IBAN/text()', namespaces=namespaces)[0] or False
                matched_invoice = False

                matched_invoice = self._match_ref(ref, ref_type)
                name = matched_invoice.number if matched_invoice else ('Ref: '+ ref)

                transactions.append({
                    'name': name,
                    'date': trans_date,
                    'amount': amount,
                    'unique_import_id': '{}-{}'.format(trans_AcctSvcrRef, entry_AcctSvcrRef),
                    'partner_name': partner_name,
                    'ref': ref,
                    'account_number':partner_acc_nmb,
                })

            statement.append({
                'name': entry_ref,
                'date': entry_date,
                'transactions': transactions
            })
        return currency, account_number, statement

    def _match_ref(self, ref, ref_type):
        if ref_type != "ISR Reference":
            return False

        invoice = self.env['account.invoice'].search([
                ('l10n_ch_isr_number','=',ref)
            ], limit=1)

        if len(invoice):
            return invoice
        else:
            return False
