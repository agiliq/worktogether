from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler

from teamwork.models import ask_team_members, send_digest


scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job('cron', ask_team_members, day_of_week='mon-fri', hour=18)
scheduler.add_job('cron', send_digest(), day_of_week='mon-fri', hour=9)

scheduler.start()