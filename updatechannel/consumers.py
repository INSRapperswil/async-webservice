from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from json import dumps


class UpdateChannelConsumer(AsyncWebsocketConsumer):
    """ A simple consumer who broadcasts update messages sent by other applications and/or celery tasks. """

    @staticmethod
    def send_update_message(message):
        """ Send a message to all connected websockets. """

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('updates', {'type': 'update_message', 'message': message})

    @staticmethod
    async def send_update_message_async(message):
        """ Send a message to all connected websockets. """

        channel_layer = get_channel_layer()
        await channel_layer.group_send('updates', {'type': 'update_message', 'message': message})

    async def connect(self):
        """ Called when a websocket connects. """

        await self.channel_layer.group_add('updates', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """ Called when a websocket disconnects. """

        await self.channel_layer.group_discard('updates', self.channel_name)

    async def update_message(self, event):
        """ Called if an update message is received. Send it to the connected websocket. """

        await self.send(text_data=dumps({'message': event['message']}))
