var app = angular.module('app', ['firebase']);
app.config(function($routeProvider) {
  $routeProvider.
    when('/', {controller: app.PlanListController, templateUrl:'{{STATIC_URL}}templates/index.html'}).
    when('/plans/:planid', {controller: app.EventListController, templateUrl:'{{STATIC_URL}}templates/plan.html'}).
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
