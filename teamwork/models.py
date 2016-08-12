import datetime
import pytz

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mass_mail
from django.db import models
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from sendgrid_events.signals import sendgrid_email_received


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    preferred_notifying_time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            time_ = datetime.time(18, 10,
                                  tzinfo=pytz.timezone(settings.TIME_ZONE))
            self.preferred_notifying_time = time_
        super(TeamMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class WorkDay(models.Model):
    person = models.ForeignKey(TeamMember)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %s" % (self.person, self.date.ctime()[:10])


class Task(models.Model):
    day = models.ForeignKey(WorkDay)
    task = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}".format(self.day)


def validate_only_one_instance(obj):
    model = obj.__class__
    if model.objects.count() > 0 and obj.id != model.objects.get().id:
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class WorkTrackerText(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return self.text

    def clean(self):
        validate_only_one_instance(self)


@receiver(sendgrid_email_received)
def receive(sender, data=None, **kwargs):
    data = data
    sender_name = data['Sender'].split('<')[0].strip()
    sender_email = data['Sender'].split('<')[1][:-1]
    subject = data.get('Subject', '')
    team_mem_tuple = TeamMember.objects.get_or_create(email=sender_email)
    person = team_mem_tuple[0]
    if team_mem_tuple[1]:
        person.name = sender_name
        person.save()
    for each in data['Body'].split('\n'):
        if each.strip().endswith('> wrote:') or each.strip() == '--':
            break
        else:
            if subject and 'change time' in subject.lower():
                try:
                    notify_time_with_tzinfo = convert_str_to_time_with_tzinfo(
                        each.strip())
                    person.preferred_notifying_time = notify_time_with_tzinfo
                    person.save()
                except ValueError, e:
                    print e
            else:
                work_day, created = WorkDay.objects.get_or_create(
                    person=person, date=datetime.datetime.now())
                Task.objects.create(day=work_day, task=each.strip())


def get_members_within_timeframe(today):
    """
    This function take a time, in 24-hour format and returns the list of
    members who set their preferred time of being notified in the next one
    hour.
    :params: - datetime
    :return: queryset
    """
    today = today.replace(minute=0, second=0)
    time_delta = datetime.timedelta(hours=1)
    next_time = today + time_delta
    return TeamMember.objects.filter(
        preferred_notifying_time__gt=today.time(),
        preferred_notifying_time__lt=next_time.time())


def ask_team_members():
    """
    Send out emails to each TeamMember asking them to send their updates for
    today by email.
    :return: None
    """
    today = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
    member_email_list = get_members_within_timeframe(today)

    if WorkTrackerText.objects.exists():
        text = WorkTrackerText.objects.first()
    else:
        text = "Tell us what did you get done today?"
    mail_list = []
    for each in member_email_list:
        mail_list.append(
            ("What have you done today? {0}".format(today.ctime()[:10]),
             "{0}".format(text),
             "hello@worksummarizer.agiliq.com",
             [each.email, ]))
    send_mass_mail((tuple(mail_list)))


def send_digest():
    last_work_day = WorkDay.objects.last().date
    team_members = TeamMember.objects.all()
    member_work = []
    for team_member in team_members:
        work_day = WorkDay.objects.get(person=team_member,
                                       date=last_work_day)
        tasks = Task.objects.filter(day=work_day)
        work_list = [task.task for task in tasks]
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
    notify_time_naive = datetime.datetime.strptime(date_str, '%H:%M')
    return notify_time_naive.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
