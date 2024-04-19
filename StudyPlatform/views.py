from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from StudyPlatform.forms import RegisterUserForm, LoginForm
from StudyPlatform.utils import DataMixin


def main(request):
    if checkCookies():
        return render(request, 'tutorPage.html')
    else:
        return redirect('/about')


def about_page(request):
    return render(request, 'about.html')


def checkCookies():
    return False


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_context_url(self):
        return reverse_lazy('main')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        if self.request.user.is_staff == 1:
            return reverse_lazy('TeacherApp:main')
        return reverse_lazy('about')


def logout_user(request):
    logout(request)
    return redirect('login')
