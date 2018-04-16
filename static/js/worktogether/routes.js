(function() {
    angular.module('worktogether')
    .config(RouteConfig);


    RouteConfig.$inject = ['$routeProvider', 'workConfig'];
    function RouteConfig($routeProvider, workConfig) {
        $routeProvider
        .when('/:date',
            {
                templateUrl: workConfig.urls.static + "js/worktogether/templates/member.html",
                controller: "WorkController",
                controllerAs: "wkCtrl"
            }
        )
        .otherwise({
            redirectTo: '/'+workConfig.date
        });
    }



})();
