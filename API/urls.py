from django.urls import include, path, re_path
from rest_framework import routers
from .views import *


urlpatterns = [
    path('tests/', TestViewSet.as_view(), name="testsApi"),
    path('users/', UsersViewSet.as_view(), name="ApiUsers"),
    path('tests/<int:test_id>/', TestQuestionsViewSet.as_view(), name="TestQuestions"),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]