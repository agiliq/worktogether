from worktogether.celery import app
from .models import send_digest, ask_team_members

@app.task(name='ask')
def ask_user():
    ask_team_members()


@app.task(name='send_digest')
def send_digest():
    send_digest()
