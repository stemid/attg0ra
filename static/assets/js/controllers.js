'use strict';

var todoAppControllers = angular.module('todoAppControllers', []);

todoAppControllers.controller('todoListCtrl', ['$scope', '$http', 
  function TodoListCtrl($scope, $http) {
    $http.get('http://localhost:8000/').
      success(function (data) {
        console.log(data);
        $scope.todos = data;
      }
    ).
      error(function (response) {
        $scope.todos = [
          {
            'title': 'No items found'
          }
        ];
      }
    );
  }
]);

todoAppControllers.controller('todoShowCtrl', ['$scope', '$routeParams',
  function ($scope, $routeParams) {
    $scope.todoId = $routeParams.todoId;
  }
]);
