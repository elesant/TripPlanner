var controllers = {};
app.controller(controllers);

controllers.EventListController = function($scope, $routeParams, angularFire) {
  var planid = $('#plan-id').text();
  var url = 'https://grouptrotter.firebaseio.com/plans/' + planid + '/events';
  var promise = angularFire(url, $scope, 'items');
  var sortableEle = null;

  function startWatch($scope) {

    $scope.planid = planid;

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
      $scope.items.push({
        name: 'test',
        id: generateGuid()
      });
    }


    sortableEle = $('.events-sortable').sortable({
        start: $scope.dragStart,
        update: $scope.dragEnd
    });
  }

    promise.then(function(todos) {
      startWatch($scope);
    });
};
