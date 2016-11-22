var app = angular.module('worktogether', ['ngRoute']);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

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

app.factory('WorkServices', ['$http', function($http) {
    var work = {};
    var taskAddUrl = TASK_CREATEURL+DATE;
    var taskDetailUrl = TASK_DETAILURL;
    work.addTask = function(_task) {
        return $http.post(taskAddUrl, {task: _task});
    };
    work.deleteTask = function(_id) {
        var url = TASK_DETAILURL.split("/");
        url.pop();
        url.push(_id);
        url = url.join("/");
        return $http.delete(url);
    };
    return work;
}]);


app.controller('WorkController', ['$http', '$q', '$filter', 'WorkServices',
    function($http, $q, $filter, workServices) {
        var url = WORKDAY_LISTURL+DATE;
        var teamUrl = TEAM_LISTURL;
        var memberId = parseInt(CURRENT_USER_ID);
        var self = this;
        var team = {};
        self.member = {};
        self.teamWork = [];
        self.newTask = "";

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

        self.addTask = function() {
            if (!self.newTask) return;
            workServices.addTask(self.newTask).then(function(resp) {
                self.member.tasks.push(resp.data);
                self.newTask = '';
            });
        };

        self.deleteTask = function(_id) {
            workServices.deleteTask(_id).then(function(){
                self.member.tasks = $filter('filter')(self.member.tasks, {id: '!'+_id});
            });
        };
    }
]);
