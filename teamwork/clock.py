from apscheduler.schedulers.blocking import BlockingScheduler

from .models import ask_team_members, send_digest


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18)
def ask():
    return ask_team_members()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=10)
def send():
    return send_digest()

sched.start()