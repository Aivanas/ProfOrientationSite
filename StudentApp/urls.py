from django.urls import path
from .views import *

app_name = "StudentApp"

urlpatterns=[
    path('', available_tests, name='available_tests'),
    path('take_test/<int:test_id>/', take_test, name='take_test'),
    path('submit_test/<int:test_id>/', submit_test, name='submit_test'),
]