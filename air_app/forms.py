from django import forms

from air_app.models import QuestionAndAnswer


class QuestionsAndAnswersForm(forms.ModelForm):
    class Meta:  # pylint: disable=R0903
        """Specifies the model and the relevant fields"""
        model = QuestionAndAnswer
        fields = '__all__'
        widgets = {
            'question_text': forms.Textarea(attrs={'cols': '', 'rows': ''}),
            'answer_text': forms.Textarea(attrs={'cols': '', 'rows': ''}),
        }


class SearchQueryForm(forms.Form):
    select_algorithm = forms.ChoiceField(choices=(
        ('boolean_model', 'Boolean model'),
        ('extended_boolean_model', 'Extended boolean model'),
        ('vector_model', 'Vector model'),
    ))

    query = forms.CharField()
