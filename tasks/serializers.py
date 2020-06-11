from tasks.models import Task
from rest_framework.serializers import ModelSerializer


class TaskSerializer(ModelSerializer):
    """ Serializer for tasks. All attributes are read only. """

    class Meta:
        model = Task
        fields = ('id', 'status', 'celery_task_id', 'started', 'finished', 'created', 'modified')
        read_only_fields = ('id', 'status', 'celery_task_id', 'started', 'finished', 'created', 'modified')
