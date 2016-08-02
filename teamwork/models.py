import datetime
import pytz

from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.exceptions import ValidationError
from django.template import Context
from django.template.loader import get_template

from sendgrid_events.signals import sendgrid_email_received


class TeamMember(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    preferred_notifying_time = models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class WorkDone(models.Model):

    person = models.ForeignKey(TeamMember)
    date = models.DateField(auto_now_add=True)
    work_done = models.TextField()

    def work_done_as_list(self):
        return self.work_done.replace('\n', '\r').split('\r')

    def __unicode__(self):
        return "%s, %s" % (self.person, self.date.ctime()[:10])


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class WorkTrackerText(models.Model):

    text = models.TextField()

    def __unicode__(self):
        return self.text

    def clean(self):
        validate_only_one_instance(self)


@receiver(sendgrid_email_received)
def receive(sender, data=None, **kwargs):
    body = ''
    data = data
    sender_name = data['Sender'].split('<')[0].strip()
    sender_email = data['Sender'].split('<')[1][:-1]
    subject = data.get('Subject', '')
    team_mem_tuple = TeamMember.objects.get_or_create(email=sender_email)
    person = team_mem_tuple[0]

    for each in data['Body'].split('\n'):
        if each.strip().endswith('> wrote:') or each.strip() == "--":
            break
        else:
            if subject and 'change time' in subject.lower():
                try:
                    notify_time_with_tzinfo = convert_str_to_time_with_tzinfo(each.strip())
                    person.preferred_notifying_time = notify_time_with_tzinfo
                    person.save()
                except ValueError:
                    pass
            else:
                body += each
    if team_mem_tuple[1]:
        person.name = sender_name
        person.save()
    work_tuple = WorkDone.objects.get_or_create(person=person,
                                                date=datetime.datetime.now())
    work_obj = work_tuple[0]
    work_obj.work_done = (work_obj.work_done + '\n' + body).strip()
    work_obj.save()


def ask_team_members():

    member_email_list = [each.email for each in TeamMember.objects.all()]
    today = datetime.datetime.now().ctime()[:10]
    text = WorkTrackerText.objects.first() if WorkTrackerText.objects.exists() \
        else "Tell us what did you get done today?"
    for each in member_email_list:
        send_mail("What have you done today? {0}".format(today),
                  "{0}".format(text),
                  "hello@worksummarizer.agiliq.com",
                  [each, ])


def send_digest():

    last_work_day = WorkDone.objects.last().date
    team_members = TeamMember.objects.all()
    member_work = []
    for team_member in team_members:
        work_list = []
        wd = team_member.workdone_set.filter(date=last_work_day)
        if wd:
            work_list = wd.first().work_done_as_list()
        member_work.append((team_member, work_list))
    template = get_template('teamwork/email.html')
    subject = 'Digest from {0}'.format(last_work_day.ctime()[:10])
    context = Context({'member_work': member_work, 'heading': subject})
    content = template.render(context)
    msg = EmailMessage(subject, content,
                       "hello@worksummarizer.agiliq.com",
                       to=['yogesh@agiliq.com', ])
    msg.content_subtype = 'html'
    msg.send()


def convert_str_to_time_with_tzinfo(date_str):
    notify_time_str = date_str
    notify_time_naive = datetime.datetime.strptime(notify_time_str, '%H:%M').time()
    notify_time_with_tzinfo = notify_time_naive.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))