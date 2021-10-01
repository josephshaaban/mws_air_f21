from django.shortcuts import render

from air_app.forms import QuestionsAndAnswersForm


def home_view(request):
    return render(request, template_name='base.html', context={
        'title': "Hi! I'm working!!",
    })


def data_entry_view(request):
    form = QuestionsAndAnswersForm()
    return render(request, template_name='', context={
        'form': form,
    })
