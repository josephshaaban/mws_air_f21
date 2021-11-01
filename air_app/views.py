import re

from django.shortcuts import render, get_object_or_404

from air_app.air_algorithms.vector_model.index import index
from air_app.air_algorithms.vector_model.search import search
from air_app.forms import QuestionsAndAnswersForm, SearchQueryForm
from air_app.models import QuestionAndAnswer


def home_view(request):
    return render(request, template_name='home.html', context={
        'title': "MWS Homework | Home",
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
        'form_submit_button': 'Post',
        'legend': 'Enter questions & answers',
    })


def search_query_view(request):
    if request.method == "POST":
        form = SearchQueryForm(request.POST)
        if form.is_valid():
            selected_algo = form.cleaned_data['select_algorithm']
            query = form.cleaned_data['query']

            if selected_algo == 'boolean_model':
                results = search(query)
            elif selected_algo == 'extended_boolean_model':
                results = search(query)
            else:
                results = search(query)

            questions = QuestionAndAnswer.objects.filter(pk__in=results)
            results = []
            for question in questions:
                colorization_template = '<span style="color: #FFFA01FF;">{query}</span>'

                question_text = question.question_text
                question_all_occurrences = set(
                    re.findall(query, question_text, flags=re.IGNORECASE))
                for occurrence in question_all_occurrences:
                    question_text = re.sub(
                        occurrence, colorization_template.format(query=occurrence), question_text)

                answer_text = question.answer_text
                answer_all_occurrences = set(
                    re.findall(query, answer_text, flags=re.IGNORECASE))
                for occurrence in answer_all_occurrences:
                    answer_text = re.sub(
                        occurrence, colorization_template.format(query=occurrence), answer_text)

                results.append({
                    'question_text': question_text,
                    'answer_text': answer_text,
                    'question_pk': question.pk,
                })

            return render(request, 'air_app/results_page.html', context={
                'results': results,
                'query': query,
            })

    form = SearchQueryForm()
    index()
    return render(request, 'air_app/data_entry.html', context={
        'form': form,
        'form_submit_button': 'Search',
        'legend': 'Search question',
    })


def display_question_view(request, pk):
    q = get_object_or_404(QuestionAndAnswer, pk=pk)
    return render(request, 'air_app/display_question_with_answer.html', context={
        'question': q,
    })
