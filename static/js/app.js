var app = angular.module('worktogether', ['ngRoute']);

// app.config(function($routeProvider) {
//     $routeProvider
//     .when('/workdone', {
//         templateUrl: STATICURL + 'templates/worktogether.html',
//     })
//     .otherwise('/workdone');
// });



app.filter('capitalize', function() {
    var toTitleCase = function(str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };
    return function(input) {
      return (!!input) ? toTitleCase(input) : '';
    };
});


app.controller('WorkController', ['$http', '$q', function($http, $q) {
    var url = WORKDAYLISTURL+DATE;
    var teamUrl = TEAMLISTURL;
    var memberId = parseInt(CURRENT_USER_ID);
    var self = this;
    var team = {};
    self.member = {};
    self.teamWork = [];

    var getTeam = $http.get(teamUrl).then(function(response) {
        angular.forEach(response.data, function(ele, idx) {
            if (team[ele.id])
                angular.extend(team[ele.id], ele);
            else
                team[ele.id] = ele;
            if (!team[ele.id].tasks) team[ele.id].tasks = [];
        });
    });

    var getWorkDay = $http.get(url).then(function(response) {
        angular.forEach(response.data, function(ele, idx) {
            var person = ele.person;
            if (team[person.id])
                angular.extend(team[person.id], {tasks: ele.task_set});
            else
                team[person.id] = {tasks: ele.task_set};
        });
    });
    $q.all([getWorkDay, getTeam]).then(function() {
        angular.forEach(team, function(val, key) {
            if (key == memberId) self.member = team[key];
            else self.teamWork.push(team[key]);
        });
    });

    self.addTask = function(_task) {
        self.member.tasks.push({id: 0, task: _task});
    };
}]);
