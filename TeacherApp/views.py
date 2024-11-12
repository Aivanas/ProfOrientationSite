from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView

from StudyPlatform.forms import TestForm, QuestionForm, ChoiceForm, UserTestForm, CommentForm
# from StudyPlatform.forms import QuestionForm
from StudyPlatform.models import User, Test, Question, Choice, UserTests, UserTestAnswers, TestResultComment
from StudyPlatform.utils import DataMixin


class MainPage(PermissionRequiredMixin, TemplateView, LoginRequiredMixin, DataMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=/teacher/')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)

    def get_permission_required(self):
        if self.request.user.is_staff:
            return 'TeacherApp.is_staff'
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_first_name'] = self.request.user.first_name
        context['user_last_name'] = self.request.user.last_name
        students_users = User.objects.filter(is_staff=False)
        context['students'] = students_users
        context['form'] = self.form_class
        context['tests'] = Test.objects.all()
        context['userTests'] = UserTests.objects.all()
        return context

    def form_valid(self, form):
        test = form.save(commit=False)
        test.slug = slugify(test.name)
        test.save()
        return redirect(f'/test/{test.slug}/')

    permission_required = 'TeacherApp.is_staff'
    template_name = 'MainPage.html'
    form_class = TestForm


# class NewTestPage(TemplateView, PermissionRequiredMixin, LoginRequiredMixin, DataMixin):
# class NewTestPage(ListView):
#     template_name = 'NewTestPage.html'
#     model = Question
#     extra_context = {
#         'form': QuestionForm()
#     }
#
#     def get_permission_required(self):
#         return ['TeacherApp.is_staff']

# def create_test(request):
#     form = QuestionForm
#     return render(request, 'NewTestPage.html', {"form": form})


def get_form(request):
    form = QuestionForm
    return JsonResponse({'form_html': render_to_string('partial_form.html', {'form': form})})


def test_detail(request):
    return render(request, 'NewTestPage.html')


def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            return redirect('TeacherApp:edit_test', test_id=test.id)
    else:
        form = TestForm()
    return render(request, 'NewTestPage.html', {'form': form})


def edit_test(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = test.questions.all()
    choices = Choice.objects.all()
    question_form = QuestionForm()
    return render(request, 'TestEditPage.html', {'test': test, 'questions': questions,
                                                 'question_form': question_form, 'choices':choices})


def add_question(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('TeacherApp:edit_test', test_id=test.id)
    else:
        form = QuestionForm()
    return render(request, 'AddQuestionPage.html', {'form': form})


def add_question_ajax(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return JsonResponse({'status': 'success', 'question_text': question.question_text})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def add_choice_question(request, test_id):
    test = Test.objects.get(id=test_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_form = ChoiceForm(request.POST)
        if question_form.is_valid() and choice_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('edit_test', test_id=test.id)
    else:
        question_form = QuestionForm()
        choice_form = ChoiceForm()
    return render(request, 'tests/add_choice_question.html', {'question_form': question_form, 'choice_form': choice_form})


def add_choice_ajax(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return JsonResponse({'status': 'success', 'choice_text': choice.choice_text, 'choice_image_url': choice.choice_image.url if choice.choice_image else ''})
        else:
            errors = {field: [error['message'] for error in errors] for field, errors in form.errors.get_json_data().items()}
            return JsonResponse({'status': 'error', 'errors': errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_question_ajax(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return JsonResponse({'status': 'success'})
def delete_choice_ajax(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    choice.delete()
    return JsonResponse({'status': 'success'})

def update_question_ajax(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'question_text': question.question_text})
        else:
            errors = {field: [error['message'] for error in error_list] for field, error_list in form.errors.get_json_data().items()}
            return JsonResponse({'status': 'error', 'errors': errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def update_choice_ajax(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES, instance=choice)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'choice_text': choice.choice_text, 'choice_image_url': choice.choice_image.url if choice.choice_image else ''})
        else:
            errors = {field: [error['message'] for error in error_list] for field, error_list in form.errors.get_json_data().items()}
            return JsonResponse({'status': 'error', 'errors': errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def assign_test(request):
    if request.method == 'POST':
        form = UserTestForm(request.POST)
        if form.is_valid():
            user_test = form.save()
            return JsonResponse({'status': 'success', 'user': user_test.user.username, 'test': user_test.test.name})
        else:
            errors = {field: [error['message'] for error in error_list] for field, error_list in form.errors.get_json_data().items()}
            return JsonResponse({'status': 'error', 'errors': errors})
    else:
        form = UserTestForm()
    return render(request, 'AssignTest.html', {'form': form})


@login_required
def view_results(request, user_test_id):
    user_test = get_object_or_404(UserTests, id=user_test_id, is_done=True)
    test = get_object_or_404(Test, id=user_test.test.id)
    comments = TestResultComment.objects.filter(user_test=user_test)
    results = []
    user_answers = UserTestAnswers.objects.filter(user=user_test.user, test=test)
    answers = []
    for answer in user_answers:
        answers.append({
            'question': answer.choice.question.question_text,
            'choice': answer.choice.choice_text,
            'correct': answer.choice.is_correct
        })
    results.append({
        'user': user_test.user,
        'answers': answers
    })

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.user_test = user_test
            comment.save()

    else:
        form = CommentForm()

    return render(request, 'ViewTestResultsPage.html',
                  {
                    'test': test,
                   'results': results,
                   "comments": comments,
                      'form': form,
                   })