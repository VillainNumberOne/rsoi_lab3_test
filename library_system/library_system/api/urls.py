from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r'^api/v1/libraries$', views.libraries),
    re_path(r'^api/v1/librarybooks$', views.librarybooks),
    re_path(r'^api/v1/libraries/info$', views.library_info),
    re_path(r'^api/v1/books/info$', views.book_info),
    re_path(r'^api/v1/books/available$', views.book_available_count),
    re_path(r'^api/v1/books/return$', views.return_book),
    re_path(r'^manage/health$', views.health),
    # re_path(r'^api/v1/libraries/([a-zA-Z]+)$', views.library_system_api),
]