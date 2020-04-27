odoo.define('kerala_flood_cess.screens', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var time = require('web.time');


    var exports = {};

    screens.ClientListScreenWidget.include({

        display_client_details: function(visibility,partner,clickpos){
            var self = this;

            if (visibility === 'edit'){
                if (!partner['id']) {
                    partner['state_id']=self.pos.company.state_id;
                }


            }
            this._super(visibility,partner,clickpos);
        }
    });
    return exports;
});
