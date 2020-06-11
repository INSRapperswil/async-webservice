from django_object_actions import DjangoObjectActions
from django.contrib import admin
from tasks.models import Task


class TaskAdmin(DjangoObjectActions, admin.ModelAdmin):
    def schedule(self, request, obj):
        obj.schedule()

    def abort(self, request, obj):
        obj.abort()

    change_actions = ('schedule', 'abort')


admin.site.register(Task, TaskAdmin)
