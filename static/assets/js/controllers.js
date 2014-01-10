'use strict';

// Här skapas objektet för att göra nya controllers med. 
var todoAppControllers = angular.module('todoAppControllers', []);

// Här används det skapade objektet för att göra en controller. 
// I controllern ska man definiera hur data ska hanteras, var data kommer ifrån.
// Till exempel här där data hämtas från en webbserver och stoppas in i $scope
// för att göras tillgängligt till en mall som använder sig av controllern. 
todoAppControllers.controller('todoListCtrl', [
  // Här listas beroenden innan själva 
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
    // Skapar en funktion för att lätt kunna återanvända den senare.
    $scope.reload();

    $scope.todo = {
      inputTitle: null,
      inputTodo: null
    };
    
    // Här kan även definieras allt möjligt annat, som t.ex. en modal med ett 
    // formulär som ska visas i samma controller
    // open_create modal
    $scope.open_create = function () {
      var createFormModal = $modal.open({
        templateUrl: 'create.html',
        controller: function ($scope, $modalInstance, $log, todo, reload) {
          // Sätt fokus i första fältet
          $('#create-title-input').focus();

          // Kopiering till lokalt scope
          $scope.todo = todo;
          $scope.reload = reload;

          // Funktionen som anropas när formuläret skickas
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
    } // Slut på open_create modal

    // Radera sak att göra
    $scope.delete = function (id) {
      $http({
        method: 'DELETE',
        url: todoSettings.apiUrl + '/' + id
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

// Controller för att visa en sak.
todoAppControllers.controller('todoShowCtrl', [
  '$scope', 
  '$routeParams',
  '$http',
  '$log',
  '$modal',
  '$sce',
  'todoSettings',

  function ($scope, $routeParams, $http, $log, $modal, $sce, todoSettings) {
    // Sak ID från adressfältet
    $scope.todoId = $routeParams.todoId;

    $scope.todo = {};

    // Saken från JSON API
    $scope.fetch = function (id) {
      $http.get(todoSettings.apiUrl + '/' + id).
        success(function (data, status) {
          $scope.todo = data[0];
          // $sce är intressant här för det är så Angular låter mig 
          // använda HTML direkt i sidan. Annars hade det varit 
          // väldigt farligt för Javascript att kunna stoppa in HTML
          // i en webbsida ofiltrerat. 
          try {
            $scope.todo.html = $sce.trustAsHtml(marked($scope.todo.text));
          } catch (e) {
            $log.error(e);
            $scope.todo.html = $sce.trustAsHtml('');
          }
        }).
        error(function (data, status, headers, config) {
          $log.error('GET fail');
        });
    }
    $scope.fetch($scope.todoId);

    // Redigera modal
    $scope.open_edit = function () {
      var editFormModal = $modal.open({
        templateUrl: 'edit.html',
        controller: function ($scope, $modalInstance, $log, todo, fetch) {
          $('#edit-title-input').focus();

          $scope.todo = todo;
          $scope.fetch = fetch;
          $log.info($scope.todo);

          $scope.update = function () {
            $http({
              method: 'UPDATE',
              headers: {
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
              },
              url: todoSettings.apiUrl + '/' + $scope.todo.id, 
              data: $scope.todo
            }).
              success(function () {
              $('#edit-form').find("textarea input[type=text], textarea").val("");
              $modalInstance.dismiss('cancel');
              $scope.fetch($scope.todo.id);
            }).
              error(function (data, status, headers, config) {
                $log.error('UPDATE fail');
                $scope.edit_status = 'Error: Failed to update';
              });
          };
          $scope.close = function () {
            $modalInstance.dismiss('cancel');
          };
        }, // End of modal controller
        resolve: {
          todo: function () {
            return $scope.todo;
          },
          fetch: function () {
            return $scope.fetch;
          }
        }
      });
    } // Slut på redigera modal
  }
]);
