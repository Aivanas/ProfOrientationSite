from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .forms import UserCreationForm, UserChangeForm
from .models import *


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username']



admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserTests)
admin.site.register(UserTestAnswers)



