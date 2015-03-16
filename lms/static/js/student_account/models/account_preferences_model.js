;(function (define, undefined) {
    'use strict';
    define([
        'gettext', 'underscore', 'backbone',
    ], function (gettext, _, Backbone) {

        var AccountPreferencesModel = Backbone.Model.extend({
            idAttribute: 'account_privacy',
            defaults: {
                account_privacy: 'private'
            }
        });

        return AccountPreferencesModel;
    })
}).call(this, define || RequireJS.define);
