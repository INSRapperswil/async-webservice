from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from updatechannel.routing import urlpatterns


application = ProtocolTypeRouter({
    # Django HTTP views are added by default
    'websocket': URLRouter(urlpatterns),
})
