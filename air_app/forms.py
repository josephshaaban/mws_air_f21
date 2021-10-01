from django import forms

from air_app.models import QuestionAndAnswer


class QuestionsAndAnswersForm(forms.ModelForm):
    class Meta:  # pylint: disable=R0903
        """Specifies the model and the relevant fields"""
        model = QuestionAndAnswer
        fields = '__all__'
