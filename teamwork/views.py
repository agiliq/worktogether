from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from sendgrid_events.signals import sendgrid_email_received
from .models import Team, Work


@receiver(sendgrid_email_received, sender=None)
def receive(sender, **kwargs):
    data = kwargs.get('data')


def send():
    pass
