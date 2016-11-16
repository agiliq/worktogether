from rest_framework import serializers
from .models import Task, WorkDay, TeamMember


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task')

    def create(self, validated_data):
        task = validated_data['task'].strip()
        person = validated_data['person']
        date = validated_data['date']
        work_day, created = WorkDay.objects.get_or_create(person=person, date=date)
        task = Task.objects.create(day=work_day, task=task)
        return task


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
