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

// Globala konstanter som kan användas för t.ex. inställningar.
todoApp.constant('todoSettings', {
  apiUrl: 'http://localhost:8000',
  maxTitleLength: 50
});

// Här definieras routes precis som i bottle.py t.ex.
// Det verkar som att man använder when och otherwise metoderna i routeProvider 
// objektet, och varje gång en av metoderna anropas så får man en ny instans 
// av routeProvider objektet tillbaka. 
// Varje anrop som ska använda sig av någon sorts dynamisk data måste även ange
// en controller som ska tillhandahålla datan. 
todoApp.config(['$routeProvider', '$httpProvider', 
  function ($routeProvider, $httpProvider) {
    // Först aktivera CORS (Cross Site JS Requests)
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];

    // Sedan definiera routes
    $routeProvider.
      when('/todos', {
        templateUrl: 'list.html',
        controller: 'todoListCtrl'
    }).
      when('/todo/:todoId', {
        templateUrl: 'show.html',
        controller: 'todoShowCtrl'
    }).
      otherwise({
        redirectTo: '/todos'
    });
  }
]);

// Här definierar jag filter som kan användas i HTML mallarna för att 
// behandla textvärden. 
// Detta är också ett exempel på injektion av beroenden i ett filter. 
todoApp.filter('cutOffString', ['todoSettings', function ($log, todoSettings) {
  return function (input, length) {
    // Så här kan jag ha ett standardvärde för ett funktionsargument. 
    length = typeof length !== 'undefined' ? length : todoSettings.maxTitleLength;

    if (input.length+3 > length) {
      return input.substr(0, length) + '...';
    } else {
      return input;
    }
  };
}]);
