app.config(function($routeProvider) {
  $routeProvider.
    when('/', {controller: app.EventListController, templateUrl:'/static/templates/index.html'}).
    when('/plans/:plan', {controller: app.EventListController, templateUrl:'/static/templates/plan.html'}).
    otherwise({redirectTo:'/'});
});