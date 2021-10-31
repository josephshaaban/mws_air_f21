from django.shortcuts import render

from air_app.air_algorithms.index import index
from air_app.forms import QuestionsAndAnswersForm


def home_view(request):
    return render(request, template_name='base.html', context={
        'title': "Hi! I'm working!!",
    })


def data_entry_view(request):
    if request.method == "POST":
        form = QuestionsAndAnswersForm(request.POST)
        form.save()
        index()

    # once ask for this page, returns an empty form
    form = QuestionsAndAnswersForm()

    return render(request, template_name='air_app/data_entry.html', context={
        'form': form,
    })
