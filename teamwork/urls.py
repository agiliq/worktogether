from django.conf.urls import patterns, url

from sendgrid_events.views import sendgrid
from . import views


urlpatterns = patterns('',
                       url('^sendgrid/',
                           sendgrid, name="sendgrid"), )
