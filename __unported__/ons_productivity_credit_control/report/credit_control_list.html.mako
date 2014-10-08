<html>
<head>
<style type="text/css">
	${css}
</style>
<script>
	var supplier = 0;
</script>
</head>
<body style="border:0; margin:0;">
<div style="padding-left: 15mm; padding-right: 15mm;">
<!-----  PROVIDE LINE BREAK FOR TEXT  ----->
<%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
%>

<br/>

   <i>${company.city or ''}, ${time.strftime("%d.%m.%Y", time.localtime())}</i> imprimé par ${user.name or ''}
<br/><br/>

<div class="header">
<span class="header" style="width: 200px;">Client</span>
<span class="header" style="width: 80px;">Numéro</span>
<span class="header" style="width: 70px;">Date</span>
<span class="header" style="width: 70px;">Echéance</span>
<span class="header" style="width: 40px;">Niveau</span>
<span class="header" style="width: 70px;">Mon.</span>
<span class="header" style="width: 70px;">Total MP</span>
<span class="header" style="width: 70px;">Payé MP</span>
<span class="header" style="width: 70px;">Solde MP</span>
<span class="header" style="width: 70px;">Cond. paiement</span>
<span class="header" style="width: 70px;">Date rappel</span>
<span class="header" style="width: 70px;">Etat</span>
</div>
<br/>

<!-----  START THE LOOP  ----->
%for o in objects :

<div class="list">

<span class="list" style="width: 200px;">
%if o.partner_id :
    ${o.partner_id.ref or ''|entity}   ${o.partner_id.name or ''|entity}  
%endif 
</span>

<span class="list" style="width: 80px;">
%if o.invoice_id :
   ${o.invoice_id.number or ''|entity}  
%endif 
</span>

<span class="list" style="width: 70px;">${formatLang(o.date, date=True)}</span>
<span class="list" style="width: 70px;">${formatLang(o.date_due, date=True)}</span>
<span class="list" style="width: 40px;">${o.level or ''|entity}</span>

<span class="list" style="width: 70px;">
%if o.currency_id :
   ${o.currency_id.name or ''|entity} 
%else :
   ${o.company_id.currency_id.name or ''|entity} 
%endif 
</span>

<span class="list"style="width: 70px;">${formatLang(o.amount_due or '', digits=get_digits(dp='Account'))}</span>
<span class="list"style="width: 70px;">${formatLang(o.amount_due - o.balance_due or '', digits=get_digits(dp='Account'))}</span>
<span class="list"style="width: 70px;">${formatLang(o.balance_due or '', digits=get_digits(dp='Account'))}</span>

<span class="list"style="width: 70px;">
%if o.invoice_id :
   ${o.invoice_id.payment_term.name or ''|entity}  
%endif 
</span>

<span class="list"style="width: 70px;">${formatLang(o.date_sent, date=True)}</span>
<span class="list"style="width: 70px;">${o.state or ''|entity}</span>

</div>

%endfor

</div>

  <p style="page-break-after:always"></p>

</body>
</html>