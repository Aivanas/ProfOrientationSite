from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import TeacherApp
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('about/', about_page, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('teacher/', include('TeacherApp.urls', namespace="TeacherApp")),
    path('profile/', show_user_profile, name='profile'),
    path('logout/', logout_user, name='logout')
]
