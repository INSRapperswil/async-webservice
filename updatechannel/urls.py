from django.urls import path
from updatechannel.views import index_view


app_name = 'updatechannel'
urlpatterns = [path('updates', index_view, name='index')]
