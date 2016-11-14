from rest_framework import serializers
from .models import Task, WorkDay, TeamMember


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task')


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'name', 'email')


class WorkDaySerializer(serializers.ModelSerializer):
    person = TeamMemberSerializer(read_only=True)
    task_set = TaskSerializer(many=True)

    class Meta:
        model = WorkDay
        fields = ('id', 'person', 'date', 'task_set')
