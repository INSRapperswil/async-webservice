from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('updatechannel.urls', namespace='updatechannel')),
    path('api/', include('tasks.urls', namespace='tasks')),
]
