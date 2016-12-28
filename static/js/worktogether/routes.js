(function() {
    angular.module('worktogether')
    .config(RouteConfig);


    RouteConfig.$inject = ['$routeProvider'];
    function RouteConfig($routeProvider) {
        $routeProvider
        .when('/:date',
            {
                templateUrl: STATICURL + "js/worktogether/templates/member.html",
                controller: "WorkController",
                controllerAs: "wkCtrl"
            }
        )
        .otherwise({
            redirectTo: '/'+DATE
        });
    }



})();
