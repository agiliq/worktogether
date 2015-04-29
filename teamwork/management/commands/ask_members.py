from django.core.management.base import BaseCommand

from teamwork.models import ask_team_members


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Ask team members what they have done today.'

    def handle(self, *args, **options):
        ask_team_members()
