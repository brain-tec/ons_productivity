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

    def _parse_file_camt(self, root):
        ns = {k or 'ns': v for k, v in root.nsmap.items()}

        def is_full_of_zeros(strg):
            pattern_zero = re.compile('^0+$')
            return bool(pattern_zero.match(strg))

        curr_cache = {c['name']: c['id'] for c in self.env['res.currency'].search_read([], ['id', 'name'])}
        statement_list = []
        unique_import_set = set([])
        currency = account_no = False
        for statement in root[0].findall('ns:Stmt', ns):
            statement_vals = {}
            statement_vals['name'] = statement.xpath('ns:Id/text()', namespaces=ns)[0]

            # Transaction Entries 0..n
            transactions = []
            sequence = 0

            # Currency 0..1
            currency = statement.xpath('ns:Acct/ns:Ccy/text() | ns:Bal/ns:Amt/@Ccy', namespaces=ns)[0]

            for entry in statement.findall('ns:Ntry', ns):
                tx_details = entry.findall('ns:NtryDtls/ns:TxDtls', ns) or entry.findall('ns:NtryDtls', ns) or [entry]
                for trans_dtls in tx_details:
                    sequence += 1
                    entry_vals = {
                        'sequence': sequence,
                    }

                    # Amount 1..1
                    if trans_dtls.xpath('ns:Amt/text()', namespaces=ns):
                        amount = float(trans_dtls.xpath('ns:Amt/text()', namespaces=ns)[0])
                    else:
                        amount = float(entry.xpath('ns:Amt/text()', namespaces=ns)[0])

                    # Credit Or Debit Indicator 1..1
                    sign = entry.xpath('ns:CdtDbtInd/text()', namespaces=ns)[0]
                    counter_party = 'Dbtr'
                    if sign == 'DBIT':
                        amount *= -1
                        counter_party = 'Cdtr'
                    entry_vals['amount'] = amount

                    # Amount currency
                    if trans_dtls.xpath('ns:AmtDtls', namespaces=ns):
                        instruc_amount = trans_dtls.xpath('ns:AmtDtls/ns:InstdAmt/ns:Amt/text()', namespaces=ns)
                        instruc_curr = trans_dtls.xpath('ns:AmtDtls/ns:InstdAmt/ns:Amt/@Ccy', namespaces=ns)
                    else:
                        instruc_amount = entry.xpath('ns:AmtDtls/ns:InstdAmt/ns:Amt/text()', namespaces=ns)
                        instruc_curr = entry.xpath('ns:AmtDtls/ns:InstdAmt/ns:Amt/@Ccy', namespaces=ns)
                    if instruc_amount and instruc_curr and instruc_curr[0] != currency and instruc_curr[0] in curr_cache:
                        amount_currency = sum([float(x) for x in instruc_amount])
                        entry_vals['amount_currency'] = amount_currency if entry_vals['amount'] > 0 else -amount_currency
                        entry_vals['currency_id'] = curr_cache[instruc_curr[0]]

                    # Date 0..1
                    transaction_date = entry.xpath('ns:ValDt/ns:Dt/text() | ns:BookgDt/ns:Dt/text() | ns:BookgDt/ns:DtTm/text()', namespaces=ns)
                    entry_vals['date'] = transaction_date and transaction_date[0] or False

                    # Name 0..1
                    ref = trans_dtls.xpath('ns:RmtInf//ns:Ref/text()', namespaces=ns)
                    ref_type = trans_dtls.xpath('ns:RmtInf//ns:CdOrPrtry/ns:Prtry/text()', namespaces=ns)
                    
                    matched_invoice = False

                    ref = ref[0] if ref else ref
                    ref_type = ref_type[0] if ref_type else ref_type
                    matched_invoice = False
                    if ref and ref_type:
                        matched_invoice = self._match_ref(ref, ref_type)

                    transaction_name = trans_dtls.xpath('ns:RmtInf/ns:Ustrd/text()', namespaces=ns)
                    # _logger.info(transaction_name)
                    transaction_name = transaction_name or entry.xpath('ns:AddtlNtryInf/text()', namespaces=ns)
                    partner_name = entry.xpath('.//ns:RltdPties/ns:%s/ns:Nm/text()' % (counter_party,), namespaces=ns)
                    entry_vals['name'] = ref if ref else ' '.join(transaction_name) if transaction_name else '/'
                    entry_vals['partner_name'] = partner_name and partner_name[0] or False
                    # Bank Account No
                    bank_account_no = entry.xpath(""".//ns:RltdPties/ns:%sAcct/ns:Id/ns:IBAN/text() |
                                                    (.//ns:%sAcct/ns:Id/ns:Othr/ns:Id)[1]/text()
                                                    """ % (counter_party, counter_party), namespaces=ns)
                    entry_vals['account_number'] = bank_account_no and bank_account_no[0] or False

                    # Reference 0..1
                    # Structured communication if available
                    if not ref:
                        # Otherwise, any of below given as reference
                        ref = trans_dtls.xpath("""ns:Refs/ns:TxId/text() | ns:Refs/ns:InstrId/text() | ns:Refs/ns:EndToEndId/text() |
                                        ns:Refs/ns:MndtId/text() | ns:Refs/ns:ChqNb/text()
                                        """, namespaces=ns)
                        entry_vals['ref'] = ref and ref[0] or False
                    else:
                        # if ISR
                        entry_vals['ref'] = (ref if not matched_invoice else matched_invoice.number) or False

                    unique_import_ref = trans_dtls.xpath('ns:Refs/ns:AcctSvcrRef/text()', namespaces=ns)
                    if unique_import_ref and not is_full_of_zeros(unique_import_ref[0]):
                        entry_ref = entry.xpath('ns:NtryRef/text()', namespaces=ns)
                        if entry_ref:
                            entry_vals['unique_import_id'] = '{}-{}'.format(unique_import_ref[0], entry_ref[0])
                        elif not entry_ref and unique_import_ref[0] not in unique_import_set:
                            entry_vals['unique_import_id'] = unique_import_ref[0]
                        else:
                            entry_vals['unique_import_id'] = '{}-{}'.format(unique_import_ref[0], sequence)
                    else:
                        entry_vals['unique_import_id'] = '{}-{}'.format(statement_vals['name'], sequence)

                    unique_import_set.add(entry_vals['unique_import_id'])
                    transactions.append(entry_vals)
            statement_vals['transactions'] = transactions

            # Start Balance
            # any (OPBD, PRCD, ITBD):
            #   OPBD : Opening Balance
            #   PRCD : Previous Closing Balance
            #   ITBD : Interim Balance (in the case of preceeding pagination)
            start_amount = float(statement.xpath("ns:Bal/ns:Tp/ns:CdOrPrtry[ns:Cd='OPBD' or ns:Cd='PRCD' or ns:Cd='ITBD']/../../ns:Amt/text()",
                                                              namespaces=ns)[0])
            # Credit Or Debit Indicator 1..1
            sign = statement.xpath('ns:Bal/ns:CdtDbtInd/text()', namespaces=ns)[0]
            if sign == 'DBIT':
                start_amount *= -1
            statement_vals['balance_start'] = start_amount
            # Ending Balance
            # Statement Date
            # any 'CLBD', 'CLAV'
            #   CLBD : Closing Balance
            #   CLAV : Closing Available
            end_amount = float(statement.xpath("ns:Bal/ns:Tp/ns:CdOrPrtry[ns:Cd='CLBD' or ns:Cd='CLAV']/../../ns:Amt/text()",
                                                              namespaces=ns)[0])
            sign = statement.xpath('ns:Bal/ns:CdtDbtInd/text()', namespaces=ns)[0]
            if sign == 'DBIT':
                end_amount *= -1
            statement_vals['balance_end_real'] = end_amount

            statement_vals['date'] = statement.xpath("ns:Bal/ns:Tp/ns:CdOrPrtry[ns:Cd='CLBD' or ns:Cd='CLAV']/../../ns:Dt/ns:Dt/text()",
                                                              namespaces=ns)[0]
            statement_list.append(statement_vals)

            # Account Number    1..1
            # if not IBAN value then... <Othr><Id> would have.
            account_no = statement.xpath('ns:Acct/ns:Id/ns:IBAN/text() | ns:Acct/ns:Id/ns:Othr/ns:Id/text()', namespaces=ns)[0]

        return currency, account_no, statement_list

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
