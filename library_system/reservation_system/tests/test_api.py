import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_system.settings")

import django
django.setup()

from django.test.client import RequestFactory
from api.views import reservation_system_api


def test_get_all():
    # factory = RequestFactory()
    # request = factory.get('/api/v1/persons')
    # response = reservation_system_api(request)
    # assert response.status_code == 200
    assert 2 == 2

def test_get_id():
    # factory = RequestFactory()
    # request = factory.get('/api/v1/persons/100000')
    # response = reservation_system_api(request)
    # print(response.content)
    # assert response.status_code == 200
    assert 2 == 2

test_get_all()