<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            .open_invoice_previous_line {
                font-style: italic;
            }

            .clearance_line {
                font-style: italic;
            }
            ${css}
        </style>
    </head>
    <body>
   
    <% import addons %>        
    <% template1 = helper.get_mako_template('ons_productivity_budget','report', 'templates', 'open_invoices_inclusion.mako.html') %>
    <% context.lookup.put_template('open_invoices_inclusion.mako.html', template1) %>
    <% template2 = helper.get_mako_template('ons_productivity_budget','report', 'templates', 'grouped_by_curr_open_invoices_inclusion.mako.html') %>
    <% context.lookup.put_template('grouped_by_curr_open_invoices_inclusion.mako.html', template2) %>
        <%setLang(user.lang)%>

        %for acc in objects:
            %if hasattr(acc, 'grouped_ledger_lines'):
               <% fl = formatLang %>
              <%include file="grouped_by_curr_open_invoices_inclusion.mako.html" args="account=acc,formatLang=fl"/>
            %else:
               <% fl = formatLang %>
              <%include file="open_invoices_inclusion.mako.html" args="account=acc,formatLang=fl"/>
            %endif
        %endfor
    </body>
</html>
