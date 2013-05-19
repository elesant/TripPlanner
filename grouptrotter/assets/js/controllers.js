var controllers = {};
app.controller(controllers);

controllers.EventListController = function($scope, $routeParams, angularFire) {
  var url = 'https://grouptrotter.firebaseio.com/plans/' + $routeParams.planid + '/events';
  var promise = angularFire(url, $scope, 'items');
  var sortableEle = null;

  function startWatch($scope) {

    $scope.dragStart = function(e, ui) {
      ui.item.data('start', ui.item.index());
    }
    $scope.dragEnd = function(e, ui) {
        var start = ui.item.data('start'),
            end = ui.item.index();
        $scope.items.splice(end, 0,
            $scope.items.splice(start, 1)[0]);
        $scope.$apply();
    }

    $scope.add = function() {
        $scope.items.push('Item: '+ $scope.items.length);
    }

    sortableEle = $('.events-sortable').sortable({
        start: $scope.dragStart,
        update: $scope.dragEnd
    });
  }

  $scope.$apply(function() {
    promise.then(function(todos) {
      startWatch($scope);
    });
  });
};

controllers.PlanListController = function($scope, $location, angularFire) {
  var promise = $.get('/api/plan/list');

  promise.then(function(data) {
    $scope.$apply(function() {
      var plan_list = data['plans'];
      $scope.plans = plan_list;
    });
  });

  $scope.addPlan = function() {
    $.ajax({
      type: "POST",
      url: '/api/plan/add/',
      data: {
        'title': $scope.title
      },
      success: function(data) {
        $scope.$apply(function() {
          $location.path('/plans/' + data.plan_id);
        });
      }
    });
  };
};