from django.shortcuts import render

from air_app.air_algorithms_ import boolean_model
from air_app.forms import QuestionsAndAnswersForm, SearchQueryForm


def home_view(request):
    return render(request, template_name='base.html', context={
        'title': "Hi! I'm working!!",
    })


def data_entry_view(request):
    if request.method == "POST":
        form = QuestionsAndAnswersForm(request.POST)
        form.save()

    # once ask for this page, returns an empty form
    form = QuestionsAndAnswersForm()

    return render(request, template_name='air_app/data_entry.html', context={
        'form': form,
    })


def search_query_view(request):
    if request.method == "POST":
        form = SearchQueryForm(request.POST)
        if form.is_valid():
            selected_algo = form.cleaned_data['select_algorithm']
            query = form.cleaned_data['query']
            if selected_algo == 'boolean_model':
                results = boolean_model(query)
            else:
                results = boolean_model(query)
            return render(request, 'results_page.html', context={'results': results})

    form = SearchQueryForm()
    return render(request, 'air_app/data_entry.html', context={
        'form': form,
    })

