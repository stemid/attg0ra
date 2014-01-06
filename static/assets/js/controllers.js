'use strict';

// Här skapas objektet för att göra nya controllers med. 
var todoAppControllers = angular.module('todoAppControllers', []);

// Här används det skapade objektet för att göra en controller. 
// I controllern ska man definiera hur data ska hanteras, var data kommer ifrån.
// Till exempel här där data hämtas från en webbserver och stoppas in i $scope
// för att göras tillgängligt till en mall som använder sig av controllern. 
todoAppControllers.controller('todoListCtrl', 
                              [ // Här listas beroenden innan själva 
                                // funktionskoden. 
                                '$scope', 
                                '$http', 
                                '$log',
                                '$modal',
                                'todoSettings',

  function ($scope, $http, $log, $modal, todoSettings) {
    // Här hämtas JSON data från en webbserver med $http tjänsten, som är
    // definierad i början som ett beroende för controllern. 
    $scope.reload = function () {
      $http.get(todoSettings.apiUrl).
        success(function (data, status) {
          $log.info('GET Success');
          $scope.todos = data;
        }).
        error(function (data, status, headers, config) {
          $log.info('GET Fail');
          $scope.todos = [];
        });
    }
    $scope.reload();

    $scope.todo = {
      inputTitle: null,
      inputTodo: null
    };
    
    // Här kan även definieras allt möjligt annat, som t.ex. en modal med ett 
    // formulär som ska visas i samma controller
    $scope.open = function () {
      var createFormModal = $modal.open({
        templateUrl: 'create.html',
        controller: function ($scope, $modalInstance, $log, todo) {
          $scope.todo = todo;
          $scope.create = function () {
            // Jag förstår inte hur man ska använda application/json här, 
            // verkar ha något med http://www.html5rocks.com/en/tutorials/cors/
            // att göra. 
            //$http.defaults.headers.post["Content-Type"] = "application/json";
            $http({
              method: 'POST',
              headers: {
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
              },
              url: todoSettings.apiUrl, 
              data: $scope.todo
            }).
              success(function () {
                $modalInstance.dismiss('cancel');
              }).
              error(function (data, status, headers, config) {
                $log.error('Could not POST, received error');
                $log.error(status);
              });
          };
          $scope.close = function () {
            $modalInstance.dismiss('cancel');
          };
        },
        resolve: {
          todo: function () {
            $log.info('resolving');
            return $scope.todo;
          }
        }
      });
    }

    // Återställ sökformulär
    $scope.reset_query = function () {
      $scope.query = '';
    }

    // Radera sak att göra
    $scope.delete = function (edited) {
      $http({
        method: 'DELETE',
        url: todoSettings.apiUrl + '/' + edited
      }).
        success(function () {
          $log.info('DELETE Success');
          $scope.reload();
        }).
        error(function () {
          $log.error('DELETE Fail');
          $scope.reload();
        });
    }

    // Slut av controller
  }
]);

todoAppControllers.controller('todoShowCtrl', ['$scope', '$routeParams',
  function ($scope, $routeParams) {
    $scope.todoId = $routeParams.todoId;
  }
]);
