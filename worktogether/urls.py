from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^sendgrid/',
                           include('sendgrid_events.urls')),
                       url(r'^admin/',
                           include(admin.site.urls)), )

urlpatterns += patterns('',
        (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )