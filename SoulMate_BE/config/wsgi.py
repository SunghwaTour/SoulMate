"""
WSGI config for SoulMate_BE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/kingbus/community/SoulMate/SoulMate_BE')
sys.path.append('/home/kingbus/community/SoulMate/SoulMate_BE/venv/lib/python3.8/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
