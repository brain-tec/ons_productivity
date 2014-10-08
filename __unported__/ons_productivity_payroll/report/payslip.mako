<html>
<head>
<style type="text/css">
	${css}
</style>
</head>
<body style="border:0; margin:0;">
<!-----  PROVIDE LINE BREAK FOR TEXT  ----->
<%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
%>

<!-----  GET THE PARTNER LANGUAGE  ----->
%for o in objects :

<% setLang(o and o.employee_id and o.employee_id.user_id and o.employee_id.user_id.lang or 'fr_FR' ) %> 
 
 
<!-- COMPANY INFO -->
<div class="company">
   <span style="padding-bottom: 3px;"><b>${company.name}</b></span><br/>
   ${company.street or ''}<br/>
   ${company.zip or ''} <u> ${company.city or ''}</u><br/>
 
%if company.phone :
   <span style="width: 60px; display:inline-block;">${_("Phone")}: </span>${company.phone or ''}<br/>
%endif
%if company.fax :
   <span style="width: 60px; display:inline-block;">${_("Fax")}: </span>${company.fax or ''}<br/>
%endif
%if company.email :
   <span style="width: 60px; display:inline-block;">${_("Email")}: </span>${company.email or ''}<br/>
 %endif
%if company.website :
   <span style="width: 60px; display:inline-block;">${_("Website")}: </span>${company.website or ''}<br/>
 %endif
 </div>



<!----- EMPLOYEE INFO ----->
<div class="address">
   ${company.city or ''}, le ${time.strftime("%d %m %Y", time.localtime())}<br/><br/>
   <b>${o.employee_id.name |entity}</b><br/>
   %if o.employee_id.address_home_id.street :
      ${o.employee_id.address_home_id.street or ''|entity}<br>  
   %endif
   %if o.employee_id.address_home_id.street2 :
      ${o.employee_id.address_home_id.street2 or ''|entity}<br>  
   %endif
      %if o.employee_id.address_home_id.zip :
      ${o.employee_id.address_home_id.zip or ''|entity}
   %endif 
   %if o.employee_id.address_home_id.city :
      <u> ${o.employee_id.address_home_id.city or ''|entity}</u><br>  
   %endif  
   %if o.employee_id.address_home_id.country_id :
      %if o.employee_id.address_home_id.country_id.code != 'CH':
	${o.employee_id.address_home_id.country_id.name}<br/>
     %endif  
   %endif  
</div>
<br/><br/><br/><br/>
<!----- DOC TYPE  ----->
<h2>${_("Payslip")}: ${dict([('01','Janvier'), 
        ('02',_('February')), 
        ('03','Mars'), 
        ('04','Avril'), 
        ('05','Mai'), 
        ('06','Juin'), 
        ('07','Juillet'), 
        ('08','Ao&ucirc;t'), 
        ('09','Septembre'), 
        ('10','Octobre'), 
        ('11','Novembre'), 
        ('12','D&eacute;cembre')])[o.date_from[5:7]].capitalize() + ' ' + o.date_from[:4]}
<!--  ${time.strftime("%%B %Y", time.strptime(o.date_from, '%Y-%m-%d')).capitalize()} -->
<!--  ${formatLang(o.date_from, date=True)} - ${formatLang(o.date_to, date=True)} -->
</h2>

<!-----  FLEXIBLE TABLE FOR INVOICE INFO  ----->
<table class="basic_table" width="100%">

<tr>
    <td class="basic_table"><b>${_("Name")}</b></td>
    <td class="basic_table">${o.employee_id.name or ''|entity}</td>
    <td class="basic_table"><b>${_("Designation")}</b></td>
    <td class="basic_table">${o.employee_id.job_id.name or ''|entity}</td>
</tr>

<tr>
    <td class="basic_table"><b>${_("AVS number")}</b></td>
    <td class="basic_table">${o.employee_id.identification_id or ''|entity}</td>
    <td class="basic_table"><b>${_("Bank Account")}</b></td>
    <td class="basic_table">${o.employee_id.bank_account_id.acc_number or ''|entity}</td>
</tr>
<tr>
    <td class="basic_table"><b>${_("Date From")}</b></td>
    <td class="basic_table">${formatLang(o.date_from, date=True)}</td>
    <td class="basic_table"><b>${_("Date To")}</b></td>
    <td class="basic_table">${formatLang(o.date_to, date=True)}</td>
</tr>
</table>

<br/><br/>


<!-----  ITEMS LIST  ----->
<div class="header">
	<span class="header" style="width: 320px;">${_("Name")}</span>
	<span class="header" style="width: 70px;">${_("Quantity")}</span>
	<span class="header" style="width: 80px; text-align: right;">${_("Rate (%)")}</span>
	<span class="header" style="width: 80px; text-align: right;">${_("Amount")}</span>
	<span class="header" style="width: 90px; text-align: right;">${_("Total")}</span>
</div>



%for line in o.line_ids :
	%if line.category_id.code != "COMP":
	<div class="list">

			%if line.category_id.code in ['NET', 'GROSS', 'TDEDUC'] :
				<span class="list" style="width: 320px; border-top: 0px;">
			%else :
				<span class="list_narrow" style="width: 320px;">
			%endif 
			%if line.category_id.code == "SNET":
				<b>${line.name | carriage_returns}</b><br/><br/>
			%else :
				${line.name | carriage_returns}
			%endif 
		</span>

		<span class="list_narrow" style="width: 70px; text-align: right;">
		      %if line.quantity != 1.00 :
		          	${ line.quantity and ("%0.2f" % line.quantity) or 0 }
		      %endif
		</span>
		
		<span class="list_narrow" style="width: 80px; text-align: right;">
			%if line.category_id.code != "NET":
				%if not line.amount_fix :
					%if line.rate != 100 :
						${"%0.2f" % (line.rate or '')} % 
					 %endif
				%endif
			%endif 
		</span>

			%if line.category_id.code in ['NET', 'GROSS', 'TDEDUC', 'BASIC'] :
				<span class="list_narrow" style="width: 80px; text-align: right;">
			%else :
				<span class="list_narrow" style="width: 80px; text-align: right;">
				%if line.rate != 100 :
					${line.amount or '0.00'}
				%endif
				%if line.category_id.code == "HS" :
					${line.amount or '0.00'}
				%endif
				%if line.category_id.code == "INDSP" :
					${line.amount or '0.00'}
				%endif
			%endif 
		</span>

			%if line.category_id.code in ['NET', 'GROSS', 'TDEDUC'] :
				<span class="list" style="width: 90px; text-align: right;">
			%else :
				<span class="list_narrow" style="width: 90px; text-align: right;">
			%endif 
			%if line.category_id.code == "SNET":
				<b>
			%endif 
			
			${line.total or '0.00'}
			
			%if line.category_id.code == "SNET":
				</b><br/><br/>
			%endif 
		</span>
	</div>
	%endif 
%endfor

</br></br></br>
<div class="notes">

</div>
    <p style="page-break-after:always"></p>
%endfor

</body>
</html>
