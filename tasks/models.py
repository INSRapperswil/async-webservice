from celery import shared_task
from datetime import datetime
from datetime import timezone
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import Model
from logging import error
from updatechannel.consumers import UpdateChannelConsumer
from webservice.celery import celery_app


class Status:
    """ Possible statuses of a task. """

    CREATED = 'Created'
    SCHEDULED = 'Scheduled'
    RUNNING = 'Running'
    FINISHED = 'Finished'
    FAILED = 'Failed'
    ABORTED = 'Aborted'

    CHOICES = (
        (CREATED, CREATED),
        (SCHEDULED, SCHEDULED),
        (RUNNING, RUNNING),
        (FINISHED, FINISHED),
        (FAILED, FAILED),
        (ABORTED, ABORTED),
    )


class Task(Model):
    """ A database model which stores parameters for a task. """

    status = CharField(choices=Status.CHOICES, default=Status.CREATED, max_length=20)
    celery_task_id = CharField(blank=True, max_length=40)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    @staticmethod
    @shared_task
    def run_task(id):
        """ Run the task in the celery worker. """

        try:
            task = Task.objects.filter(id=id).get()
            task.running()
            task.run()
            task.refresh_from_db()
            task.finish()
        except Task.DoesNotExist:
            pass
        except Exception as exception:
            error(exception)
            task.fail()

    def run(self):
        """ The task itself. We just wait a bit and return. """
        from time import sleep
        sleep(5)

    def announce(self):
        """ Announce changes through the update channel. """

        UpdateChannelConsumer.send_update_message({
            'event': 'task-updated',
            'model': self.__class__.__name__,
            'data': {
                'task': self.id,
                'status': self.status,
                'started': self.started.isoformat() if self.started else None,
                'finished': self.finished.isoformat() if self.finished else None,
                'created': self.created.isoformat() if self.created else None,
                'modified': self.modified.isoformat() if self.modified else None,
            }
        })

    def schedule(self):
        """ Schedule the task. """

        if self.status in (Status.CREATED, Status.FINISHED, Status.FAILED, Status.ABORTED):
            self.status = Status.SCHEDULED
            self.started = None
            self.finished = None
            self.save()
            self.celery_task_id = self.run_task.apply_async(args=[self.id])
            self.save()
            self.announce()
            return True

        return False

    def running(self):
        """ Set the task to running. """

        if self.status in (Status.SCHEDULED):
            self.status = Status.RUNNING
            self.started = datetime.now(timezone.utc)
            self.save()
            self.announce()
            return True

        return False

    def finish(self):
        """ Set the task to finished. """

        if self.status == Status.RUNNING:
            self.status = Status.FINISHED
            self.finished = datetime.now(timezone.utc)
            self.save()
            self.announce()
            return True

        return False

    def fail(self):
        """ Set the task to failed. """

        if self.status == Status.RUNNING:
            self.status = Status.FAILED
            self.finished = datetime.now(timezone.utc)
            self.save()
            self.announce()
            return True

        return False

    def abort(self, terminate=False):
        """ Abort the task. """
        if self.status in (Status.SCHEDULED, Status.RUNNING) or terminate:
            self.status = Status.ABORTED
            self.finished = datetime.now(timezone.utc)
            self.save()
            celery_app.control.revoke(self.celery_task_id, terminate=terminate)
            self.announce()
            return True

        return False

    def __str__(self):
        return f'Task: Status: {self.status}'
