<html>
<head>
<style type="text/css">
	${css}
</style>
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
	<span class="header" style="width: 140px;">Compte</span>
	<span class="header" style="width: 708px; text-align: center;"> </span>
	<span class="header" style="width: 95px; text-align: right;">Total</span>
	
	<span class="header" style="width: 140px;"> </span>
	<span class="header" style="width: 59px;">Janvier</span>
	<span class="header" style="width: 59px;">Février</span>
	<span class="header" style="width: 59px;">Mars</span>
	<span class="header" style="width: 59px;">Avril</span>
	<span class="header" style="width: 59px;">Mai</span>
	<span class="header" style="width: 59px;">Juin</span>
	<span class="header" style="width: 59px;">Juillet</span>
	<span class="header" style="width: 59px;">Août</span>
	<span class="header" style="width: 59px;">Septembre</span>
	<span class="header" style="width: 59px;">Octobre</span>
	<span class="header" style="width: 59px;">Novembre</span>
	<span class="header" style="width: 59px;">Décembre</span>
	<span class="header" style="width: 95px; text-align: right;"> </span>
</div>


<div class="list">
<!-----  START THE LOOP  ----->
%for o in objects :
	%if len(o.onsp_budget_pos_ids) > 0:
		<span class="list" style="width: 140px;">${o.code or ''} / ${o.name or '' |entity}</span>
		%for line in o.onsp_budget_pos_ids :
			%for subline in line.period_ids :
				<span class="list" style="width: 56px; text-align: right; border-right: 1px dotted gray; padding-right: 2px;">${formatLang(subline.amount or '0.00', digits=get_digits(dp='Account'))}</span>
			%endfor
		<span class="list" style="width: 95px; text-align: right;">${formatLang(line.amount or '0.00', digits=get_digits(dp='Account'))}</span><br/>
		%endfor
	%endif
%endfor
</div>

</div>

<p style="page-break-after:always"></p>

</body>
</html>
