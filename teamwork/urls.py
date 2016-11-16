from django.conf.urls import url, include

from .views import member_work_view, delete_task, edit_task, add_task
from .views_api import WorkDayListView, TaskDetailView, TeamMemberListView, TaskCreateView


api_patterns = [
    url(r'^workday/(?P<date>([0-9-]*)\w*)$', WorkDayListView.as_view(), name="workday-list"),
    url(r'^teammembers/$', TeamMemberListView.as_view(), name="members-list"),
    url(r'^tasks/(?P<pk>([0-9]+))$', TaskDetailView.as_view(), name="task-detail"),
    url(r'^tasks/(?P<date>([0-9-]*))', TaskCreateView.as_view(), name="task-create")
]


urlpatterns = [
    url(r'^remove_task/$', delete_task, name='remove_task'),
    url(r'^edit_task/$', edit_task, name='edit_task'),
    url(r'^add_task/(?P<date>([0-9-]*)\w*)$', add_task, name='add_task'),
    url(r'^date/(?P<date>([0-9-]*)\w*)$', member_work_view, name='day_summary'),
    url(r'api/', include(api_patterns))
]
