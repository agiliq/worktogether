from django.core.management.base import BaseCommand

from teamwork.models import send_digest


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Send the digest of work done.'

    def handle(self, *args, **options):
        send_digest()
