web: gunicorn worktogether.wsgi --log-file -
worker: celery worker --app=worktogether.app
clock: python teamwork/clock.py