import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import TeamMember, WorkDay, Task


def get_work_summary(date):
    """
    Creates a dictionary of all the members with their updates for a given
    date.
    :params: date datetime obj
    :return: dict
    """
    team = TeamMember.objects.all()
    work_day = WorkDay.objects.filter(date=date)
    summary = {}
    for member in team:
        try:
            day = work_day.get(person=member)
            tasks = Task.objects.filter(day=day)
            summary[member] = tasks
        except ObjectDoesNotExist as e:
            print e
            summary[member] = ['No updated for today']

    return summary


def member_work_view(request, date=None):
    if not date:
        date = datetime.datetime.now()
        return redirect(reverse('day_summary', kwargs={'date': str(date)[:10]}, ))
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    summary = get_work_summary(date)

    return render(request, "teamwork/base.html", {'summary': summary})


@csrf_exempt
def delete_task(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        task_id = request.POST.get('id')
        # Task.objects.get(id=request.POST.get(task_id)).delete()
        return HttpResponse(json.dumps({'id': task_id}))
    else:
        return redirect(reverse('date/'))


@csrf_exempt
def edit_task(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        task_id = request.POST.get('id')
        return HttpResponse(json.dumps({'id': task_id}))
    else:
        return redirect(reverse('date/'))
