from django.contrib import admin

from .models import TeamMember, WorkDay, Task, WorkTrackerText


class WorkDayAdmin(admin.ModelAdmin):

    list_display = ['date', 'person']

admin.site.register(TeamMember)
admin.site.register(WorkDay, WorkDayAdmin)
admin.site.register(Task)
admin.site.register(WorkTrackerText)
