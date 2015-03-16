;(function (define, undefined) {
    'use strict';
    define([
        'gettext', 'jquery', 'underscore', 'backbone',
        'js/student_account/models/account_preferences_model',
        'js/student_account/models/account_settings_models',
        'js/student_profile/views/learner_profile_view',
        'js/student_account/views/account_settings_fields'
    ], function (gettext, $, _, Backbone, AccountPreferencesModel, AccountSettingsModel, LearnerProfileEditView,
                 AccountSettingsFieldViews) {

        var setupLearnerProfile = function (options) {

            var learnerProfileElement = $('.wrapper-profile');

            var accountPreferencesModel = new AccountPreferencesModel();
            accountPreferencesModel.url = options['preferences_api_url'];

            var accountSettingsModel = new AccountSettingsModel();
            accountSettingsModel.url = options['accounts_api_url'];

            var editable = options['readonly'] ? 'never': 'toggle';

            var accountPrivacyFieldView = new AccountSettingsFieldViews.AccountPrivacyFieldView({
                model: accountPreferencesModel,
                required: true,
                editable: 'always',
                showMessages: false,
                title: gettext('edX learners can see my:'),
                valueAttribute: "account_privacy",
                options: [
                    ['private', gettext('Limited Profile')],
                    ['all_users', gettext('Full Profile')]
                ],
                helpMessage: '',
                accountSettingsPageUrl: options['account_settings_page_url']
            });

            var usernameFieldView = new AccountSettingsFieldViews.ReadonlyFieldView({
                    model: accountSettingsModel,
                    valueAttribute: "username",
                    helpMessage: ""
            });

            var sectionOneFieldViews = [
                new AccountSettingsFieldViews.DropdownFieldView({
                    model: accountSettingsModel,
                    required: false,
                    editable: editable,
                    showMessages: false,
                    iconName: 'fa-map-marker',
                    placeholderValue: gettext('Add country'),
                    valueAttribute: "country",
                    options: options['country_options'],
                    helpMessage: ''
                }),

                new AccountSettingsFieldViews.DropdownFieldView({
                    model: accountSettingsModel,
                    required: false,
                    editable: editable,
                    showMessages: false,
                    iconName: 'fa-comment fa-flip-horizontal',
                    placeholderValue: gettext('Add language'),
                    valueAttribute: "language",
                    options: options['language_options'],
                    helpMessage: '',
                })
            ];

            var sectionTwoFieldViews = [
                new AccountSettingsFieldViews.TextareaFieldView({
                    model: accountSettingsModel,
                    editable: editable,
                    showMessages: false,
                    title: gettext('About me'),
                    placeholderValue: gettext("Tell other edX learners a little about yourself, where you're from, what your interests are, why you joined edX, what you hope to learn..."),
                    valueAttribute: "bio",
                    helpMessage: ''
                })
            ];

            accountSettingsModel.fetch().done(function () {
                accountPreferencesModel.fetch({complete: function () {
                    new LearnerProfileEditView({
                        el: learnerProfileElement,
                        readonly: options['readonly'],
                        has_preferences_access: options['has_preferences_access'],
                        accountSettingsModel: accountSettingsModel,
                        preferencesModel: accountPreferencesModel,
                        accountPrivacyFieldView: accountPrivacyFieldView,
                        usernameFieldView: usernameFieldView,
                        sectionOneFieldViews: sectionOneFieldViews,
                        sectionTwoFieldViews: sectionTwoFieldViews
                    }).render();
                }});
            });
        };

        return setupLearnerProfile;
    })
}).call(this, define || RequireJS.define);