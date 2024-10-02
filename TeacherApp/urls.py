from django.urls import path
from .views import *

app_name = "TeacherApp"

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('tests/create/', create_test, name='create_test'),
    path('tests/<int:test_id>', edit_test, name='edit_test'),
    path('tests/<int:test_id>/add_question/', add_question, name='add_question'),
    path('tests/<int:test_id>/add_question_ajax/', add_question_ajax, name='add_question_ajax'),
    path('question/<int:question_id>/add_choice/', add_choice_ajax, name='add_choice_ajax'),
    path('question/<int:question_id>/delete/', delete_question_ajax, name='delete_question_ajax'),
    path('choice/<int:choice_id>/delete/', delete_choice_ajax, name='delete_choice_ajax'),
    path('question/<int:question_id>/update/', update_question_ajax, name='update_question_ajax'),
    path('choice/<int:choice_id>/update/', update_choice_ajax, name='update_choice_ajax'),
    path('assign-test/', assign_test, name='assign_test'),
    path('view_results/<int:test_id>/', view_results, name='view_results'),
]