from django.conf.urls import patterns, url

from .views import member_work_view, delete_task, edit_task

urlpatterns = patterns('',
                       url(r'^remove_task/$', delete_task, name='remove_task'),
                       url(r'^edit_task/$', edit_task, name='edit_task'),
                       url(r'^date/(?P<date>([0-9-]*)\w*)$', member_work_view,
                           name='day_summary'), )
