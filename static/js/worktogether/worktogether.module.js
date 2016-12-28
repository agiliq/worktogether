(function() {

angular.module('worktogether', ['ngRoute'])
.controller('WorkController', WorkController)
.config(CsrfConfig);


CsrfConfig.$inject = ['$httpProvider'];
function CsrfConfig($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}



WorkController.$inject = ['$q', '$filter', '$routeParams', 'WorkServices'];
function WorkController($q, $filter, $routeParams, workServices) {
    var memberId = parseInt(CURRENT_USER_ID);
    var self = this;
    var team = {};
    self.member = {};
    self.teamWork = [];
    self.newTask = "";
    self.date = $routeParams.date;

    var teamData = workServices.getTeamData();
    var workDayData = workServices.getWorkDayData(self.date);

    teamData.then(function(response) {
        angular.forEach(response.data, function(ele, idx) {
            if (team[ele.id])
                angular.extend(team[ele.id], ele);
            else
                team[ele.id] = ele;
            if (!team[ele.id].tasks) team[ele.id].tasks = [];
        });
    });

    workDayData.then(function(response) {
        angular.forEach(response.data, function(ele, idx) {
            var person = ele.person;
            if (team[person.id])
                angular.extend(team[person.id], {tasks: ele.task_set});
            else
                team[person.id] = {tasks: ele.task_set};
        });
    });

    $q.all([workDayData, teamData]).then(function() {
        angular.forEach(team, function(val, key) {
            if (key == memberId) self.member = team[key];
            else self.teamWork.push(team[key]);
        });
    });

    self.addTask = function() {
        if (!self.newTask) return;
        workServices.addTask(self.date, self.newTask).then(function(resp) {
            self.member.tasks.push(resp.data);
            self.newTask = '';
        });
    };

    self.deleteTask = function(_id) {
        workServices.deleteTask(_id).then(function(){
            self.member.tasks = $filter('filter')(self.member.tasks, {id: '!'+_id});
        });
    };

    self.updateTask = function(_id, update) {
        var failed = true;
        if (!update.trim().length) return failed;
        workServices.updateTask(_id, update).then(function(){
            angular.forEach(self.member.tasks, function(task, idx) {
                if (task.id == _id) task.task = update;
            });
            return !failed;
        });
    };
}

})();
