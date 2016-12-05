odoo.define('ons_productivity_employee_barcode.EmployeeWidget',function (require) {

    "use strict";

    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var web_client = require('web.web_client');
    var Model = require('web.Model');
    var framework = require('web.framework');
    var session = require('web.session');
    var utils = require('web.utils');

    var EmployeeWidget = Widget.extend({

        template:'ons_productivity_employee_barcode.EmployeeWidget',
        events: {
            'click .employee_barcode_exit': 'exit_employee',
        },

        init: function(parent){
            this._super(parent);
            
            var Employee = new Model('hr.employee');
            Employee.call('set_employee_barcode', ['No employee'], {}).then(function (result) {})
            this.current_employee = "No employee";
            var User = new Model('res.users');
            User.query(['ons_needs_barcode']).filter([['id', '=', session.uid]]).all().then(function (user) {
                if (user.length > 0) {
                    if (user[0].ons_needs_barcode) {
                        framework.blockUI();
                    }
                }
            });
            var keys = [];
            var time_between_input = 500;
            var last_timestamp = 0;
            var self = this;
            

            $(document).keydown(function(e){
                // Don't catch non-printable keys for which Firefox triggers a keypress
                if (e.key === "ArrowLeft" || e.key === "ArrowRight" ||
                e.key === "ArrowUp" || e.key === "ArrowDown" ||
                e.key === "Escape" || e.key === "Tab" ||
                /F\d\d?/.test(e.key)) {
                    return;
                }
                if (e.ctrlKey || e.metaKey || e.altKey)
                    return;
                if (last_timestamp == 0 || Date.now() - last_timestamp < time_between_input || keys.length == 0) {
                    if (e.key === "Enter") {
                        if (keys) {
                            var Employee = new Model('hr.employee');
                            var barcode = keys.join('');
                            Employee.query(['name']).filter([['ons_barcode', '=', keys.join('')]]).all().then(function (employees) {
                                if (employees.length > 0) {
                                    self.current_employee = employees[0].name;;
                                    Employee.call('set_employee_barcode', [barcode], {}).then(function (result) {
                                        framework.unblockUI();
                                    })
                                    self.renderElement();
                                }
                            });
                            keys = [];
                        }

                    }
                    else {
                        keys.push(e.key);
                    }
                }
                else {
                    keys = [];
                }
                last_timestamp = Date.now()
            });
        },
        exit_employee: function(ev) {
            var self = this; 
            self.current_employee = 'No employee';
            self.renderElement();
            framework.blockUI();
        },
        renderElement: function() {
            this._super();
            var self = this;
            this.$el.find('.employee_barcode')[0].innerHTML = this.current_employee;
        },


    });

SystrayMenu.Items.push(EmployeeWidget);

});