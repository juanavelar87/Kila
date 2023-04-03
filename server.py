import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from serverless_wsgi import handle_request


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = get_wsgi_application()


def handler(event, context):
    response = handle_request(event, application)
    response['headers']['content-type'] = 'text/html; charset=utf-8'
    response['headers']['cache-control'] = 'max-age=0, no-cache, no-store, must-revalidate'
    response['headers']['pragma'] = 'no-cache'
    response['headers']['expires'] = '0'
    return response