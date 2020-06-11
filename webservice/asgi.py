import os

from channels.routing import get_default_application
from django import setup


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webservice.settings')

setup()
application = get_default_application()
