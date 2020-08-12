"""
WSGI config for iptv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ['SECRET_KEY'] = 'sample_key'
os.environ['DB_NAME'] = 'iptv'
os.environ['DB_USER'] = 'iptvuser'
os.environ['DB_PASSWORD'] = 'newpassword'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = "5432"
os.environ['CORS_WHITELIST'] = 'http://localhost:4200'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iptv.settings')

application = get_wsgi_application()
