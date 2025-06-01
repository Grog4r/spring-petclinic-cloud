// scripts/appointment-form/appointment-form.js

'use strict';

angular.module('appointmentForm', ['ui.router'])
    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider
            .state('appointmentNew', {
                parent: 'app',
                url: '/appointments/new',
                template: '<appointment-form></appointment-form>'
            });
    }]);