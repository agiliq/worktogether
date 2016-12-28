import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from .models import TeamMember, WorkDay, Task


@login_required
def member_work_view(request, date=None):
    if not date:
        date = datetime.datetime.now()
        return redirect(reverse('day_summary',
                                kwargs={'date': str(date)[:10]}, ))
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    team = TeamMember.objects.all()
    work_day = WorkDay.objects.filter(date=date)
    summary = {}
    for member in team:
        try:
            day = work_day.get(person=member)
            tasks = Task.objects.filter(day=day).order_by('id')
            summary[member] = tasks
        except ObjectDoesNotExist as e:
            print e
            summary[member] = ['No updated for today']
    context = {
        'summary': summary,
        'date': date
    }
    try:
        context['current_member'] = request.user.teammember
    except:
        pass
    return render(request, "teamwork/base.html", context)


class MemberWorkListView(TemplateView):
    template_name = "teamwork/base.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberWorkListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberWorkListView, self).get_context_data(**kwargs)
        today = datetime.datetime.now().date()
        context['date'] = today
        try:
            context['current_member'] = self.request.user.teammember
        except:
            pass
        return context


class UserProfileView(TemplateView):
    template_name = "teamwork/profile.html"
