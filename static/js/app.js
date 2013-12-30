'use strict';

/* App Module */

var phonecatApp = angular.module('phonecatApp', [
  'ngRoute',
  'phonecatAnimations',
  'phonecatControllers',
  'phonecatFilters',
  'phonecatServices'
]);

phonecatApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/api/v1/project', {
        templateUrl: 'static/partials/phone-list.html',
        controller: 'ProjectListCtrl'
      }).
      when('/api/v1/project/:projectId/', {
        templateUrl: 'static/partials/phone-detail.html',
        controller: 'ProjectDetailCtrl'
      }).
      otherwise({
        redirectTo: '/api/v1/project'
      });
  }]);