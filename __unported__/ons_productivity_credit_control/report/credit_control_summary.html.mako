<html>
<head>
<style type="text/css">
	${css}
</style>
<script>
	var sum = 0;
	var extra = 0;
	var total = 0;

/**  
 * Repeat a string `n`-times (recursive)
 * @param {Number} n - The times to repeat the string.
 * @param {String} d - A delimiter between each string.
 */

String.prototype.repeat = function (n, d) {
    return --n ? this + (d || "") + this.repeat(n, d) : "" + this;
}

function formatFloat(num,casasDec,sepDecimal,sepMilhar) {
    if (num < 0)
    {
        num = -num;
        sinal = -1;
    } else
        sinal = 1;
    var resposta = "";
    var part = "";
    if (num != Math.floor(num)) // decimal values present
    {
        part = Math.round((num-Math.floor(num))*Math.pow(10,casasDec)).toString(); // transforms decimal part into integer (rounded)
        while (part.length < casasDec)
            part = '0'+part;
        if (casasDec > 0)
        {
            resposta = sepDecimal+part;
            num = Math.floor(num);
        } else
            num = Math.round(num);
    } // end of decimal part
    while (num > 0) // integer part
    {
        part = (num - Math.floor(num/1000)*1000).toString(); // part = three less significant digits
        num = Math.floor(num/1000);
        if (num > 0)
            while (part.length < 3) // 123.023.123  if sepMilhar = '.'
                part = '0'+part; // 023
        resposta = part+resposta;
        if (num > 0)
            resposta = sepMilhar+resposta;
    }
     if (resposta.indexOf(sepDecimal) < 0) {
         resposta += sepDecimal
     }
    var pos = resposta.indexOf(sepDecimal)
    if (resposta.length - pos < casasDec+1) {
        resposta = (resposta + "0".repeat(casasDec))
        resposta = resposta.substr(0,pos+casasDec+1)
    }
    if (sinal < 0)
        resposta = '-'+resposta;
    return resposta;
}
</script>
</head>
<body style="border:0; margin:0;">
<div style="padding-left: 15mm; padding-right: 15mm;">
<!-----  PROVIDE LINE BREAK FOR TEXT  ----->
<%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
%>

<!-----  GET THE PARTNER LANGUAGE  ----->
%for inv in objects :
    <% setLang(inv.partner_id.lang) %> 
 <br/>
<!----- CUSTOMER INFO ----->
<div class="address" style="margin-left: 400px;">
<!--- DISPLAY THE PARTNER OR THE CONTACT NAME --->
   <b>
%if not inv.partner_id.is_company:
      %if inv.partner_id.title :
         ${inv.partner_id.title.shortcut or ''|entity} 
     %endif
%endif
      ${inv.partner_id.name |entity}
   </b><br/>
     %if inv.partner_id.function :
      <i>${inv.partner_id.function or ''|entity}</i><br>  
   %endif 
<!--- DISPLAY THE PARTNER NAME IF CONTACT WAS USED --->
    %if inv.partner_id.parent_id :
      <b>${inv.partner_id.parent_id.name or ''|entity}</b><br>  
   %endif  
   %if inv.partner_id.street :
      ${inv.partner_id.street or ''|entity}<br>  
   %endif
   %if inv.partner_id.street2 :
      ${inv.partner_id.street2 or ''|entity}<br>  
   %endif
      %if inv.partner_id.zip :
      ${inv.partner_id.zip or ''|entity}
   %endif 
   %if inv.partner_id.city :
       ${inv.partner_id.city or ''|entity}<br>  
   %endif  
   %if inv.partner_id.country_id.code :
      %if inv.partner_id.country_id.code != 'CH':
         ${inv.partner_id.country_id.code} - ${inv.partner_id.country_id.name}<br/>
      %endif   
   %endif 
</div>

</br></br>
<!----- DISPLAY LEVEL  ----->
%if inv.current_policy_level :
    <h1>${inv.current_policy_level.name  or ''|entity}</h1>
%endif

<br/>
Date : ${time.strftime("%d.%m.%Y", time.localtime())}
</br></br></br>

<!----- DISPLAY MESSAGE  ----->
${inv.current_policy_level.custom_text  or ''  | carriage_returns}
</br></br>

<script>
	sum = 0.00;
	extra = 0.00;
	total = 0.00;
</script>

<!-----  ITEMS LIST  ----->
<div class="header">
	<span class="header" style="width: 90px;">No. facture</span>
	<span class="header" style="width: 80px;">Date</span>
	<span class="header" style="width: 75px;">Echéance</span>
	<span class="header" style="width: 65px; text-align: right;">Retard</span>
	<span class="header" style="width: 75px; text-align: right;">Rappel No.</span>
	<span class="header" style="width: 80px; text-align: right;">Montant</span>
	<span class="header" style="width: 80px; text-align: right;">Payé</span>
	<span class="header" style="width: 80px; text-align: right;">Solde</span>
</div>

%for line in inv.credit_control_line_ids :
<div class="list">
	<span class="list" style="width: 90px;">
           %if line.invoice_id :
		${line.invoice_id.number or '' |entity}
	  %endif
        </span>
	<span class="list" style="width: 80px;">
           %if line.invoice_id :
		${formatLang(line.invoice_id.date_invoice, date=True)}
	  %endif
        </span>
	<span class="list" style="width: 75px;">${formatLang(line.date_due, date=True)}</span>
	<span class="list" style="width: 65px; text-align: right;">${(datetime.datetime.strptime(line.date.format('%Y-%m-%d'),'%Y-%m-%d')-datetime.datetime.strptime(line.date_due.format('%Y-%m-%d'),'%Y-%m-%d')).days} j.</span>
	<span class="list" style="width: 75px; text-align: right;">${ "%0.0f" % (line.level)}</span>
	<span class="list" style="width: 80px; text-align: right;">${formatLang(line.amount_due or 0.0)}</span>
	<span class="list" style="width: 80px; text-align: right;">${formatLang(line.amount_due - line.balance_due or 0.0)}</span>
	<span class="list" style="width: 80px; text-align: right;">${formatLang(line.balance_due or 0.0)}</span>
</div>

<!-----  COMPUTE EXTRA AMOUNT  ----->
%if line.level == 2:
   <script>
      extra += 20;
      total += 20;
   </script>
%endif
%if line.level == 3:
    <script>
       extra += 50;
       total += 50;
    </script>
%endif

<script>
	sum += parseFloat("${line.balance_due or 0.0}".replace("'",""));
	total += parseFloat("${line.balance_due or 0.0}".replace("'",""));
</script>
%endfor

<div class="total" style="border-top:0px;">

<!----- 
<script>
if (extra > 0.0) { 
       document.write('<span class="list" style="width: 450px; min-height: 20px;">&nbsp;</span>');
       document.write('<span class="list" style="width: 120px; min-height: 20px;">&nbsp;</span>');
       document.write('<span class="list" style="width: 80px; text-align: right; min-height: 20px;">' + formatFloat(sum,2,'.',"'") + '</span>');
   }
</script>
<script>
if (extra > 0.0) { 
       document.write('<span class="list" style="width: 450px; min-height: 20px;">&nbsp;</span>');
       document.write('<span class="list" style="width: 120px; min-height: 20px;">+Frais de rappel</span>');
       document.write('<span class="list" style="width: 80px; text-align: right; min-height: 20px;">' + formatFloat(extra,2,'.',"'") + '.00</span>');
   }
</script>
----->

     <span class="header" style="width: 490px; min-height: 20px;">&nbsp;</span>
     <span class="header" style="width: 100px; min-height: 20px;">Total</span>
     <span class="header" style="width: 52px; text-align: right; border-bottom:1px solid black; min-height: 20px;">
        <script> 
           document.write( formatFloat(sum,2,'.',"'") ); 
        </script>
    </span>
</div>
<br/>

<!---- ADD A PAGE FOR THE CREDIT NOTES   ---->

%if len(inv.partner_id.ons_refund_ids) > 0:
<script>
	refund = 0.00;
</script>
	<p style="page-break-after:always"></p>
	<br/>
	<!----- CUSTOMER INFO ----->
	<div class="address" style="margin-left: 400px;">
	<!--- DISPLAY THE PARTNER OR THE CONTACT NAME --->
	</div>
	</br></br>
	<!----- DISPLAY LEVEL  ----->
	<h1>Liste de vos avoirs</h1>
	<br/>
	Date : ${time.strftime("%d.%m.%Y", time.localtime())}
	</br></br></br>
	<!----- DISPLAY MESSAGE  ----->
	</br></br>
	<div class="header">
		<span class="header" style="width: 180px;">No. facture</span>
		<span class="header" style="width: 120px;">Date</span>
		<span class="header" style="width: 112px; text-align: right;">Montant de l'avoir</span>
		<span class="header" style="width: 110px; text-align: right;">Déjà utilisé</span>
		<span class="header" style="width: 110px; text-align: right;">Solde de l'avoir</span>
	</div>
	%for line in inv.partner_id.ons_refund_ids :
		%if line.state == 'open' :
		<div class="list">
			<span class="list" style="width: 180px;">${line.number or '' |entity}</span>
			<span class="list" style="width: 120px;">${formatLang(line.date_invoice, date=True)}</span>
			<span class="list" style="width: 112px; text-align: right;">${formatLang(line.amount_total or 0.0)}</span>
			<span class="list" style="width: 110px; text-align: right;">${formatLang(line.amount_total - line.residual or 0.0)}</span>
			<span class="list" style="width: 110px; text-align: right;">${formatLang(line.residual or 0.0)}</span>
		</div>
		
		<script>
			refund += parseFloat("${line.residual or 0.0}".replace("'",""));
		</script>
		
		%endif
	%endfor

	<div class="total" style="border-top:0px;">
		<span class="header" style="width: 490px; min-height: 20px;">&nbsp;</span>
		<span class="header" style="width: 100px; min-height: 20px;">Total</span>
		<span class="header" style="width: 52px; text-align: right; border-bottom:1px solid black; min-height: 20px;">
			<script> 
			document.write( formatFloat(refund,2,'.',"'") ); 
			</script>
		</span>
	</div>
%endif
  <p style="page-break-after:always"></p>

%endfor
</div>
</body>
</html>
