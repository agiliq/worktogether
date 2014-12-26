import datetime

from django.db import models
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from sendgrid_events.signals import sendgrid_email_received


class TeamMember(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.name


class WorkDone(models.Model):

    person = models.ForeignKey(TeamMember)
    date = models.DateField(auto_now_add=True)
    work_done = models.TextField()

    def work_done_as_list(self):
        return self.work_done.split('\n')

    def __unicode__(self):
        return "%s, %s" % (self.person, self.date.ctime()[:10])


@receiver(sendgrid_email_received)
def receive(sender, **kwargs):
    body = ''
    data = kwargs.get('data')
    sender_name = data['Sender'].split('<')[0].strip()
    sender_email = data['Sender'].split('<')[1][:-1]
    for each in data['Body'].split('\n'):
        if each.strip().endswith('> wrote:') or each.strip() == "--":
            break
        else:
            if each.strip():
                body += each
    team_mem_tuple = TeamMember.objects.get_or_create(email=sender_email)
    person = team_mem_tuple[0]
    if team_mem_tuple[1]:
        person.name = sender_name
        person.save()
    work_tuple = WorkDone.objects.get_or_create(person=person,
                                                date=datetime.datetime.now())
    work_obj = work_tuple[0]
    work_obj.work_done = (work_obj.work_done + '\n' + body).strip()
    work_obj.save()


def send():

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterdays_work = WorkDone.objects.filter(date=yesterday)
    template = get_template('teamwork/email.html')
    context = Context({'work_list': yesterdays_work})
    content = template.render(context)
    subject = 'Agiliq digest from {0}'.yesterday.ctime()[:10]
    msg = EmailMessage(subject, content,
                       "hello@worksummarizer.agiliq.com",
                       to=['team@agiliq.com',])
    msg.content_subtype='html'
    msg.send()
