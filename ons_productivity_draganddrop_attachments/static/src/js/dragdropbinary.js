odoo.define('ons_productivity_mail_draganddrop_attachments.dragdropbinary', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.Model');
var FieldMany2ManyBinaryMultiFiles = core.form_widget_registry.map.many2many_binary

var dragdropMany2many = FieldMany2ManyBinaryMultiFiles.extend({
	initialize_content: function()  {
		this._super();
		self = this;

		var parent = self.__parentedParent;
		var content = this.$el

		content.on(
			    'dragenter', function(e) {
					content.css("border", "3px solid green");
					e.preventDefault();
					e.stopPropagation();
				}
			);
			content.on(
			    'dragleave', function(e) {
					content.css("border", "none");
					e.preventDefault();
					e.stopPropagation();
				}
			);
			content.on(
			    'dragover', function(e) {
			    	content.css("border", "3px solid green");
					e.preventDefault();
					e.stopPropagation();
				}
			);
			content.on(
			    'drop', function(e) {
			    	content.css("border", "none");
			    	e.preventDefault();
					e.stopPropagation();
					var files = e.originalEvent.dataTransfer.files;
					for (var i = 0; i < files.length; i++) {
						var myFile = files.item(i);
						var myFileReader = new FileReader()
						myFileReader.onload = (function(myFile) {
								return function(e) {
									if(e.target.result) {
										var datas = e.target.result.split(",")[1]
										var res_id = 0
										if (parent.datarecord.id){
											res_id = parent.datarecord.id
										}
										self.ds_file.call('create', [
											{
												'name': myFile.name,
												'datas_fname': myFile.name,
												'res_model': parent.model,
												'res_id': 0,
												'datas': datas,
											}
										]).then(function (datas) {
											var values = _.clone(self.get('value'));
								            values.push(datas);
								            self.set({value: values});
											self.render_value();
										});
									}
								}
							}
						)(myFile);
						myFileReader.readAsDataURL(myFile);
					}
				});
	}
})

core.form_widget_registry.add('many2many_binary', dragdropMany2many);

})