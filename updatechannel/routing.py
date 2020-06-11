from django.urls import path
from updatechannel.consumers import UpdateChannelConsumer


urlpatterns = [
    path('ws/updates/', UpdateChannelConsumer),
]
