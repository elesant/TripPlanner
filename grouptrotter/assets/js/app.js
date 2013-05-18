var app = angular.module('app', ['firebase']);
app.config(function($routeProvider) {
  $routeProvider.
    when('/', {controller: app.PlanListController, templateUrl:'/static/templates/index.html'}).
    when('/plans', {controller: app.EventListController, templateUrl:'/static/templates/plan.html'}).
    otherwise({redirectTo:'/'});
});

$(document).ready(function () {
  var offsetFn = function() {
    return $('#affix-sidebar').position().top;
  };
  $('#affix-sidebar').affix({
    offset: {top: offsetFn}
  });

  $('.navbar-fixed-top').affix();
});