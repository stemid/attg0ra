'use strict';

var todoApp = angular.module('todoApp', [
  'ngRoute',
  'todoAppControllers'
]);

todoApp.config(['$routeProvider',
  function ($routeProvider) {
    $routeProvider.
      when('/todos', {
        templateUrl: 'list.html',
        controller: 'todoListCtrl'
    }).
      when('/todo/:todoId', {
        templateUrl: 'todo.html',
        controller: 'todoShowCtrl'
    }).
      otherwise({
        redirectTo: '/todos'
    });
  }
]);
