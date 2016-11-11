import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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
    return render(request, "teamwork/base.html", {
        'summary': summary, 'date': str(date)[:10]})


@csrf_exempt
@login_required
def add_task(request, date):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 'method not supported'}))
    # ToDo Make sure logged in user can add tasks for him only
    person = None
    _task = request.POST.get('newtask', '').strip()
    _userid = request.POST.get('userid', '')
    try:
        person = TeamMember.objects.get(id=_userid)
    except:
        pass
    if not person or not _task:
        return HttpResponse(json.dumps({'status': 'error'}))
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    work_day, created = WorkDay.objects.get_or_create(person=person, date=date)
    task = Task.objects.create(day=work_day, task=_task)
    return HttpResponse(json.dumps({'status': 'success', 'taskid': task.id}))


@csrf_exempt
@login_required
def delete_task(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 'method not supported'}))
    # ToDo make sure only authorized user can delete task
    try:
        Task.objects.get(id=request.POST.get("id", "")).delete()
    except Task.DoesNotExist:
        return HttpResponse(json.dumps({'status': 'error'}))
    return HttpResponse(json.dumps({'status': 'success'}))


@csrf_exempt
def edit_task(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        return HttpResponse(json.dumps({}))
    else:
        return redirect(reverse('date/'))
