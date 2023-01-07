from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r'^api/v1/libraries/$', views.libraries),
    re_path(r'^api/v1/libraries$', views.libraries),
    re_path(r'^api/v1/libraries/(?P<library_uid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/books$', views.libraries),
    re_path(r'^api/v1/reservations$', views.reservations),
    re_path(r'^api/v1/reservations/(?P<reservation_uid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/return$', views.return_book),
    re_path(r'^api/v1/rating$', views.rating),
    re_path(r'^manage/health$', views.health),
]