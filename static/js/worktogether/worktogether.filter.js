(function() {

    angular.module('worktogether')
    .filter('capitalize', CapitalizeFilter)
    .filter('isEmpty', CheckEmptyFilter);

    function CapitalizeFilter() {
        var toTitleCase = function(str) {
            return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        };
        return function(input) {
            return (!!input) ? toTitleCase(input) : '';
        };
    }

    function CheckEmptyFilter() {
        return function(obj) {
            return angular.equals({}, obj);
        };
    }
    
})();
