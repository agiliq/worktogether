from .models import WorkDay, TeamMember, Task
from .serializers import WorkDaySerializer, TeamMemberSerializer, TaskSerializer
from rest_framework import generics


class WorkDayListView(generics.ListAPIView):
    queryset = WorkDay.objects.all()
    serializer_class = WorkDaySerializer

    def get_queryset(self):
        date = self.kwargs.get('date', '')
        if date:
            return self.queryset.filter(date=date)
        return self.queryset.all()


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
