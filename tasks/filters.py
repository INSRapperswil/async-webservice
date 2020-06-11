from django_filters import MultipleChoiceFilter
from django_filters.rest_framework import FilterSet
from tasks.models import Task
from tasks.models import Status


class TaskFilter(FilterSet):
    """ Filter for tasks. Allows filtering by status. """

    status = MultipleChoiceFilter(choices=Status.CHOICES)

    class Meta:
        model = Task
        fields = ('status',)
