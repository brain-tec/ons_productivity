odoo.define('ons_productivity_sale_crm.dashboard', function (require) {
"use strict";

var core = require('web.core');
var formats = require('web.formats');
var Model = require('web.Model');
var session = require('web.session');
var KanbanView = require('web_kanban.KanbanView');

var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;

var OnspSalesCrmDashboardView = KanbanView.extend({
    display_name: _lt('Dashboard'),
    icon: 'fa-dashboard',
    view_type: "onsp_sales_crm_dashboard",
    searchview_hidden: true,
    events: {
        'click .o_dashboard_action': 'on_dashboard_action_clicked',
    },

    fetch_data: function() {
        return new Model('crm.lead')
            .call('retrieve_onsp_sales_dashboard', [], { context: this.dataset.context });
    },

    render: function() {
        var super_render = this._super;
        var self = this;

        return this.fetch_data().then(function(result){
            self.show_demo = false;

            var sales_dashboard = QWeb.render('ons_productivity_sale_crm.OnspSalesDashboard', {
                widget: self,
                show_demo: self.show_demo,
                values: result,
            });
            super_render.call(self);

            // The whole content must be set to display=block...
            self.$el.css({display:'block'});
            self.$el.attr('class', 'o_cannot_create')
            // ... but the lower kanban part must remain "flex"
            self.$el.wrapInner( "<div class='o_kanban_view o_kanban_small_column o_kanban_grouped ui-sortable' style='display: flex;'/>" )

            //$(sales_dashboard).prependTo(self.$el);
            self.$el.prepend($(sales_dashboard));
        });
    },

    on_dashboard_action_clicked: function(ev){
        ev.preventDefault();

        var self = this;
        var $action = $(ev.currentTarget);
        var action_name = $action.attr('name');
        var action_extra = $action.data('extra');
        var additional_context = {}

        // TODO: find a better way to add defaults to search view
        if (action_name === 'calendar.action_calendar_event') {
            additional_context['search_default_mymeetings'] = 1;
        } else if (action_name === 'crm.crm_lead_action_activities') {
            if (action_extra === 'today') {
                additional_context['search_default_today'] = 1;
            } else if (action_extra === 'this_week') {
                additional_context['search_default_this_week'] = 1;
            } else if (action_extra === 'overdue') {
                additional_context['search_default_overdue'] = 1;
            }
        } else if (action_name === 'crm.action_your_pipeline') {
            if (action_extra === 'overdue') {
                additional_context['search_default_overdue'] = 1;
            }
        }

        new Model("ir.model.data")
            .call("xmlid_to_res_id", [action_name])
            .then(function(data) {
                if (data){
                   self.do_action(data, {additional_context: additional_context});
                }
            });
    },

    on_change_input_target: function(e) {
        var self = this;
        var $input = $(e.target);
        var target_name = $input.attr('name');
        var target_value = $input.val();

        if(isNaN(target_value)) {
            this.do_warn(_t("Wrong value entered!"), _t("Only Integer Value should be valid."));
        } else {
            this._updated = new Model('crm.lead')
                            .call('modify_target_sales_dashboard', [target_name, parseInt(target_value)])
                            .then(function() {
                                return self.render();
                            });
        }
    },

    render_monetary_field: function(value, currency_id) {
        var currency = session.get_currency(currency_id);
        var digits_precision = currency && currency.digits;
        value = formats.format_value(value || 0, {type: "float", digits: digits_precision});
        if (currency) {
            if (currency.position === "after") {
                value += currency.symbol;
            } else {
                value = currency.symbol + value;
            }
        }
        return value;
    },
});

core.view_registry.add('onsp_sales_crm_dashboard', OnspSalesCrmDashboardView);

return OnspSalesCrmDashboardView

});
