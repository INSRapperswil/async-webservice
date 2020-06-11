from channels.testing import WebsocketCommunicator
from json import loads
from pytest import mark
from updatechannel.consumers import UpdateChannelConsumer


@mark.asyncio
async def test_update_channel_consumer():
    communicator = WebsocketCommunicator(UpdateChannelConsumer, "/testws/")
    connected, subprotocol = await communicator.connect()
    assert connected is True

    await UpdateChannelConsumer.send_update_message_async({'a': 1, 'b': 'x'})
    response = await communicator.receive_from()
    assert loads(response) == {'message': {'a': 1, 'b': 'x'}}

    await communicator.disconnect()
