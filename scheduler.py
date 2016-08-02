import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from teamwork.models import ask_team_members, send_digest

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.DEBUG)

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

sched = BlockingScheduler({
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
    'executors': {
        'default': ProcessPoolExecutor(max_workers=1)
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'Asia/Kolkata',
})

sched.add_job(ask_team_members, 'cron', day_of_week='mon-fri', hour=17, minute=8, timezone=settings.TIME_ZONE)
sched.add_job(send_digest, 'cron', day_of_week='mon-fri', hour=17, minute=10, timezone=settings.TIME_ZONE)
sched.start()
