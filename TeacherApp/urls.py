from django.urls import path
from .views import *

app_name = "TeacherApp"

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
]