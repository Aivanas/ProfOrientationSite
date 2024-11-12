from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from StudentApp.forms import TestForm
from StudyPlatform.models import UserTests, Test, UserTestAnswers, Choice, TestResultComment


@login_required
def available_tests(request):
    done_user_tests = UserTests.objects.filter(user=request.user, is_done=True)
    user_tests = UserTests.objects.filter(user=request.user, is_done=False)
    tests = [user_test.test for user_test in user_tests]
    comments = TestResultComment.objects.filter(user_test__in=done_user_tests)

    context = {
        'done_user_tests': done_user_tests,
        'user_tests': user_tests,
        'tests': tests,
        'comments': comments,
    }
    return render(request, 'StudentMainPage.html', context)


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_test = get_object_or_404(UserTests, user=request.user, test=test)

    if request.method == 'POST':
        form = TestForm(request.POST, test=test)
        if form.is_valid():
            for question in test.questions.all():
                choice_id = form.cleaned_data[f'question_{question.id}']
                choice = get_object_or_404(Choice, id=choice_id)
                UserTestAnswers.objects.create(user=request.user, test=test, choice=choice)
            user_test.is_done = True
            user_test.save()
            return redirect('StudentApp:available_tests')
    else:
        form = TestForm(test=test)

    questions_with_choices = []
    for question in test.questions.all():
        choices = []
        for choice in question.choices.all():
            choices.append({
                'id': choice.id,
                'text': choice.choice_text,
                'image': choice.choice_image.url if choice.choice_image else None
            })
        questions_with_choices.append({
            'question': question,
            'choices': choices
        })

    return render(request, 'PassingTestPage.html', {
        'form': form,
        'test': test,
        'questions_with_choices': questions_with_choices
    })

@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        form = TestForm(request.POST, test=test)
        if form.is_valid():
            for question in test.questions.all():
                choice_id = form.cleaned_data[f'question_{question.id}']
                choice = get_object_or_404(Choice, id=choice_id)
                UserTestAnswers.objects.create(user=request.user, test=test, choice=choice)
            user_test = get_object_or_404(UserTests, user=request.user, test=test)
            user_test.is_done = True
            user_test.save()
            return redirect('StudentApp:available_tests')
    return redirect('StudentApp:take_test', test_id=test_id)


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


    return render(request, 'WatchingResultsPage.html',
                  {
                    'test': test,
                   'results': results,
                   "comments": comments,
                   })
