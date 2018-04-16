(function() {

    angular.module('worktogether')
    .factory('WorkServices', WorkServices);

    WorkServices.$inject = ['$http', 'workConfig'];
    function WorkServices($http, workConfig) {
        var work = {};

        var getTaskDetailUrl = function(_id) {
            var url = workConfig.urls.taskDetail.split("/");
            url.pop();
            url.push(_id);
            return url.join("/");
        };

        work.getWorkDayData = function(date) {
            var workDayUrl = workConfig.urls.workdayList+date;
            return $http.get(workDayUrl);
        };

        work.getTeamData = function() {
            return $http.get(workConfig.urls.teamList);
        };

        work.addTask = function(date, _task) {
            var taskAddUrl = workConfig.urls.taskCreate+date;
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
