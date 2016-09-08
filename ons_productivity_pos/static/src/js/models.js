odoo.define('ons_productivity_pos.models', function (require) {
"use strict";

var models = require('point_of_sale.models');
var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
    initialize: function(attributes,options){
        _super_order.initialize.apply(this,arguments);
        var pos_config = this.pos.config;
        var def_cust = pos_config.pos_default_customer;
        if(def_cust){
            var client = this.pos.db.get_partner_by_id(def_cust[0]);
            if(client){
                this.set('client',client);            }
            }
    }

});

});
