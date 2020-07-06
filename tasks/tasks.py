from celery import shared_task
from updatechannel.consumers import UpdateChannelConsumer


@shared_task
def my_periodic_task(message):
    UpdateChannelConsumer.send_update_message({
        'event': 'periodic-task',
        'data': {
            'message': message
        }
    })
