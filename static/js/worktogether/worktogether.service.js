(function() {

    angular.module('worktogether')
    .factory('WorkServices', WorkServices);


    WorkServices.$inject = ['$http'];
    function WorkServices($http) {
        var work = {};
        var teamUrl = TEAM_LISTURL;

        var getTaskDetailUrl = function(_id) {
            var url = TASK_DETAILURL.split("/");
            url.pop();
            url.push(_id);
            return url.join("/");
        };

        work.getWorkDayData = function(date) {
            var workDayUrl = WORKDAY_LISTURL+date;
            return $http.get(workDayUrl);
        };

        work.getTeamData = function() {
            return $http.get(teamUrl);
        };

        work.addTask = function(date, _task) {
            var taskAddUrl = TASK_CREATEURL+date;
            return $http.post(taskAddUrl, {task: _task});
        };
        work.deleteTask = function(_id) {
            var url = getTaskDetailUrl(_id);
            return $http.delete(url);
        };
        work.updateTask = function(_id, newTask) {
            var url = getTaskDetailUrl(_id);
            return $http.put(url, {id: _id, task: newTask});
        };
        return work;
    }
    

})();
