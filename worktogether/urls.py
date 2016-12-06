from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView

admin.autodiscover()


urlpatterns = [
    url(r'^sendgrid/', include('sendgrid_events.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^teamwork/', include('teamwork.urls')),
    url(r'^$', RedirectView.as_view(url='/teamwork/day'))
]

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$',
                         'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT}), )

urlpatterns += [
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
