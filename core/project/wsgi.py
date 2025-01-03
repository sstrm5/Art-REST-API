"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.project.settings.local')
sys.path.append('/home/django_projects/MyProject')
sys.path.append('/home/django_projects/MyProject/myproject')

application = get_wsgi_application()
