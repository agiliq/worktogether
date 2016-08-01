from django.contrib import admin

from .models import TeamMember, WorkDone, WorkTrackerText


class WorkDoneAdmin(admin.ModelAdmin):

    list_display = ['date', 'person']

admin.site.register(TeamMember)
admin.site.register(WorkDone, WorkDoneAdmin)
admin.site.register(WorkTrackerText)
