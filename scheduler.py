from pytz import utc
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from teamwork.models import ask_team_members, send_digest


log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.DEBUG)

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job(ask_team_members, 'cron', day_of_week='mon-fri', hour=12, minute=30)
scheduler.add_job(send_digest, 'cron', day_of_week='mon-fri', hour=3, minute=30)

scheduler.start()
