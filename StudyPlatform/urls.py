from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('about/', about_page, name='about'),
    path('login/', login_page, name='login'),
    path('register/', RegisterUser.as_view(), name='register')
]
