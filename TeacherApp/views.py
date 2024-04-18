from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from StudyPlatform.utils import DataMixin


# Create your views here.

class MainPage(PermissionRequiredMixin, TemplateView, LoginRequiredMixin, DataMixin):
    template_name = 'MainPage.html'