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

scheduler = BackgroundScheduler({
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': 'sqlite:///jobs.sqlite'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'Asia/Kolkata',
    })

scheduler.add_job(ask_team_members, 'cron', day_of_week='mon-fri', hour=14, minute=10)
scheduler.add_job(send_digest, 'cron', day_of_week='mon-fri', hour=14, minute=30)

scheduler.start()
