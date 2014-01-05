'use strict';

// Detta skapar den grundläggande applikationen som allt annat ska byggas på.
// Här anges namnet på applikationen som sedan skapar objektet todoApp. 
// Samt beroenden till applikationen, som i detta fallet är ngRoute för att 
// kunna definiera routes, och alla controllers från controllers.js. 
var todoApp = angular.module('todoApp', [
  'ngRoute',
  'ui.bootstrap',
  'todoAppControllers'
]);

todoApp.constant('todoSettings', {
  apiUrl: 'http://192.168.22.135:8000/'
});

// Här definieras routes precis som i bottle.py t.ex.
// Det verkar som att man använder when och otherwise metoderna i routeProvider 
// objektet, och varje gång en av metoderna anropas så får man en ny instans 
// av routeProvider objektet tillbaka. 
// Varje anrop som ska använda sig av någon sorts dynamisk data måste även ange
// en controller som ska tillhandahålla datan. 
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
