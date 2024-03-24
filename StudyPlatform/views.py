from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from StudyPlatform.utils import DataMixin


def main(request):
    if checkCookies():
        return render(request, 'tutorPage.html')
    else:
        return redirect('/about')


def about_page(request):
    return render(request, 'about.html')


def login_page(request):
    return render(request, 'login.html')


def checkCookies():
    return False


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_context_url(self):
        return reverse_lazy('main')
