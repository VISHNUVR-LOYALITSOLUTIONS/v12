odoo.define('kerala_flood_cess.load_models', function (require) {
    var models = require('point_of_sale.models');
    var time = require('web.time');


    var exports = {};

    models.load_fields("res.company", "state_id");
    models.load_fields("res.partner", "x_gstin");

    models.load_models([

        {
            model: 'res.country.state',
            fields: [],
            loaded: function(self,states){
                self.states = states;
                self.company.state = null;
                for (var i = 0; i < states.length; i++) {
                    if (states[i].id === self.company.state_id[0]){
                        self.company.state = states[i];
                    }
                }
            },
        },



    ]);

    return exports;
});
