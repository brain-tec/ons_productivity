<html>
<!--
  File: report/report_webkit_stats.mako
  Module: ons_productivity_stats

  Created by cyp@open-net.ch

  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
-->
<head>
<style type="text/css">
${css}
</style>
</head>	
<body> 
%for o in objects:
    <div style="text-align:center"><h1>TABLEAU DE BORD - ${o.name|entity}</h1></div>
    <div style="text-align:center">Semaine du ${formatLang(o.date_from, date=True)} au ${formatLang(o.date_to, date=True)}</div>
    <br/>
    <table class="list_table" width="100%">
    <tr>
        <th width="25%"> </th>
        <th width="25%" style="text-align:right;">Total HT commandes</th>
        <th width="25%" style="text-align:right;">Total HT facturation<br/>"Brouillon"</th>
        <th width="25%" style="text-align:right;">Total HT facturation<br/>"Ouverte"</th>
    </tr>

    %for line in o.main_line_ids:
        <tr>
        <td width="25%"> </td>
        <td width="25%" style="text-align:right;">${line.currency_id.name|entity} ${ '%1.2f' % line.sale_stat|entity}</td>
        <td width="25%" style="text-align:right;">${line.currency_id.name|entity} ${ '%1.2f' % line.draft_inv_stat|entity}</td>
        <td width="25%" style="text-align:right;">${line.currency_id.name|entity} ${ '%1.2f' % line.opened_inv_stat|entity}</td>
        </tr>
    %endfor
    <tr><td colspan="4"><br/></td></tr>

    %for line in o.user_line_ids:
        %for sub_line in line.currency_line_ids:
            <tr>
            <td width="25%">
                %if sub_line.name.id == o.comp_currency_id.id:
                    ${line.name.name|entity}</td>
                %endif
            </td>
            <td width="25%" style="text-align:right;">${sub_line.name.name|entity} ${ '%1.2f' % sub_line.sale_stat|entity}</td>
            <td width="25%" style="text-align:right;">${sub_line.name.name|entity} ${ '%1.2f' % sub_line.draft_inv_stat|entity}</td>
            <td width="25%" style="text-align:right;">${sub_line.name.name|entity} ${ '%1.2f' % sub_line.opened_inv_stat|entity}</td>
            </tr>
        %endfor
    %endfor
    </table>
    <p style="page-break-after:always"></p>
%endfor
</body>
</html>
