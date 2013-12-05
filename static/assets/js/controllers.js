'use strict';

var todoAppControllers = angular.module('todoAppControllers', []);

todoAppControllers.controller('TodoListCtrl', ['$scope', '$http', 
  function TodoListCtrl($scope, $http) {
    $http.get('http://localhost:9001/').success(function (data) {
      $scope.todos = data;
    });

    $scope.orderProp = 'id';
  }
]);

todoAppControllers.controller('TodoShowCtrl', ['$scope', '$routeParams',
  function ($scope, $routeParams) {
    $scope.todoId = $routeParams.todoId;
  }
]);
