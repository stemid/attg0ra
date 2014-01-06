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
          $scope.todos = data;
        }).
        error(function (data, status, headers, config) {
          $log.error('GET Fail');
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
        controller: function ($scope, $modalInstance, $log, todo, reload) {
          // Sätt fokus i första fältet
          $('#create-title-input').focus();

          $scope.todo = todo;
          $scope.reload = reload;

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
                // Återställ alla fält
                $('#create-form').find("textarea input[type=text], textarea").val("");

                // Stäng modalrutan
                $modalInstance.dismiss('cancel');

                // Ladda om listan med saker
                $scope.reload();
              }).
              error(function (data, status, headers, config) {
                $log.error('POST fail');
                $scope.post_status = 'Error: Failed to post';
              });
          };
          $scope.close = function () {
            $modalInstance.dismiss('cancel');
          };
        },
        resolve: { // Här lägger man till saker från ovanstående scope
          todo: function () {
            return $scope.todo;
          },
          reload: function () {
            return $scope.reload;
          }
        }
      });
    }

    $scope.show = function (date) {
      var showItemModal = $modal.open({
        templateUrl: 'show.html',
        controller: function ($scope, $modalInstance, $log, reload) {
          $log.info(date);
          $scope.reload = reload;
          // Gör annat specifikt för show.html mallen
        },
        resolve: {
          reload: function () {
            return $scope.reload;
          }
        }
      });
    }

    // Radera sak att göra
    $scope.delete = function (edited) {
      $http({
        method: 'DELETE',
        url: todoSettings.apiUrl + '/' + edited
      }).
        success(function () {
          $scope.reload();
        }).
        error(function () {
          $log.error('DELETE Fail');
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
