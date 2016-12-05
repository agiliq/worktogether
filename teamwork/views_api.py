from datetime import datetime
from .models import WorkDay, TeamMember, Task
from .serializers import (WorkDaySerializer, TeamMemberSerializer,
                          TaskSerializer)
from rest_framework import generics
from rest_framework import permissions
from rest_framework.serializers import ValidationError


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.day.get_user() == request.user


class WorkDayListView(generics.ListAPIView):
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer

    def get_queryset(self):
        date = self.kwargs.get('date', '')
        if not date:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        return self.queryset.filter(date=date)


class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class WorkDayDetailView(generics.ListAPIView):
    lookup_field = 'date'
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        errors = []
        date_str = self.kwargs.get("date", "")
        try:
            person = self.request.user.teammember
        except TeamMember.DoesNotExist:
            errors.append('Related teammember doesnt exist for user')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            errors.append('Invalid Date format. Required YYYY-MM-DD')
        if errors:
            raise ValidationError(errors)
        serializer.save(person=person, date=date)
