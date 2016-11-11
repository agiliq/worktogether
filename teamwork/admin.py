from django.contrib import admin

from .models import TeamMember, WorkDay, Task, WorkTrackerText


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class WorkDayAdmin(admin.ModelAdmin):
    list_display = ['date', 'person']
    list_filter = ['person']
    inlines = [TaskInline]


admin.site.register(TeamMember)
admin.site.register(WorkDay, WorkDayAdmin)
admin.site.register(Task)
admin.site.register(WorkTrackerText)
