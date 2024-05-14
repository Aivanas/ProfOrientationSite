from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from StudyPlatform.models import User
from StudyPlatform.utils import DataMixin


# Create your views here.

class MainPage(PermissionRequiredMixin, TemplateView, LoginRequiredMixin, DataMixin):
    def get_permission_required(self):
        return ['TeacherApp.is_staff']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_first_name'] = self.request.user.first_name
        context['user_last_name'] = self.request.user.last_name

        students_users = User.objects.filter(is_staff=False)
        context['students'] = students_users

        return context

    template_name = 'MainPage.html'