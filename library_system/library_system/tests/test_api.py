import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_system.settings")

import django
django.setup()

from django.test.client import RequestFactory
from api.views import library_system_api
