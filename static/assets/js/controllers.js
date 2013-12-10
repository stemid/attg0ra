'use strict';

// Här skapas objektet för att göra nya controllers med. 
var todoAppControllers = angular.module('todoAppControllers', []);

// Här används det skapade objektet för att göra en controller. 
// I controllern ska man definiera hur data ska hanteras, var data kommer ifrån.
// Till exempel här där data hämtas från en webbserver och stoppas in i $scope
// för att göras tillgängligt till en mall som använder sig av controllern. 
todoAppControllers.controller('todoListCtrl', 
                              [ // Här listas beroenden innan själva funktionskoden. 
                                '$scope', 
                                '$http', 
                                '$log',
                                '$modal',

  function TodoListCtrl($scope, $http, $log, $modal) {
    // Här hämtas JSON data från en webbserver med $http tjänsten, som är definierad 
    // i början som ett beroende för controllern. 
    $http.get('http://localhost:8000/').
      success(function (data, status) {
        $log.info('HTTP GET returned: ' + data + ', status: ' + status);
        $scope.todos = data;
      }
    ).
      error(function (data, status, headers, config) {
        $log.info('HTTP GET returned error: ' + status);
        $scope.todos = [
          {
            'title': 'No items found'
          }
        ];
      }
    );
    
    // Här kan även definieras allt möjligt annat, som t.ex. en modal med ett formulär 
    // som ska visas i samma controller
    $scope.open = function () {
      var createFormModal = $modal.open({
        templateUrl: 'create.html',
        controller: 'ModalCreateCtrl',
        resolve: {
          todo: function () {
            $log.info('resolving');
            return $scope.todo;
          }
        }
      });
    }
  }
]);

// Här definieras modal controllern som anropas från TodoListCtrl.
// En controller är i sin enklaste form bara en funktion med ett visst symbolnamn
// som går att slå upp i någon sorts JS-namnrymd. 
var ModalCreateCtrl = function ($scope, $modalInstance, $log) {
  $scope.empty = {};

  $log.info('in the modal controller');

  $scope.create = function (input) {
    var $form = $('#create-form');
    var data = $form.serialize();
    $http.post('http://localhost:8000/', data).
      success(function (data) {
        $log.info(data);
      });
  };
}

todoAppControllers.controller('todoShowCtrl', ['$scope', '$routeParams',
  function ($scope, $routeParams) {
    $scope.todoId = $routeParams.todoId;
  }
]);
