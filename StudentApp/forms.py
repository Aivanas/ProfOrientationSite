from django import forms


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        test = kwargs.pop('test')
        super(TestForm, self).__init__(*args, **kwargs)
        for question in test.questions.all():
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, label=question.question_text)