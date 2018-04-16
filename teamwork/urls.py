from django.conf.urls import url, include

from .views import member_work_view, MemberWorkListView, UserProfileView
from .views_api import (WorkDayListView, TaskDetailView,
                        TeamMemberListView, TaskCreateView, HeatMapList)


api_patterns = [
    url(r'^workday/(?P<date>([0-9-]*)\w*)$',
        WorkDayListView.as_view(), name="workday-list"),
    url(r'^teammembers/$',
        TeamMemberListView.as_view(), name="members-list"),
    url(r'^tasks/(?P<pk>([0-9]+))$',
        TaskDetailView.as_view(), name="task-detail"),
    url(r'^tasks/(?P<date>([0-9-]*))',
        TaskCreateView.as_view(), name="task-create"),
    url(r'^tasks_heatmap$',
        HeatMapList.as_view(), name="task-heatmap")

]


urlpatterns = [
    url(r'^date/(?P<date>([0-9-]*)\w*)$',
        member_work_view, name='day_summary'),
    url(r'^day$', MemberWorkListView.as_view(), name='day-details'),
    url(r'^user-profile$', UserProfileView.as_view(), name='user-profile'),
    url(r'api/', include(api_patterns))
]
