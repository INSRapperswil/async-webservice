from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer
from updatechannel.mixins import NotifyMixin


class TaskViewSet(NotifyMixin, ModelViewSet):
    """ The view set for tasks.

    Implements the GET/POST/PUT methods and our custom POSTS for starting/stopping tasks.

    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    @action(detail=True, methods=['post'])
    def run(self, request, pk):
        """ Run the task synchronously. """

        task = self.get_object()
        task.run()
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk):
        """ Run the task asynchronously. """

        task = self.get_object()
        task.schedule()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def abort(self, request, pk):
        """ Abort the task (asynchronously). """

        task = self.get_object()
        task.abort()
        return Response(status=status.HTTP_202_ACCEPTED)
