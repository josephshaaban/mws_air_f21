import math
import os
import pickle
import shelve
from collections import Counter

from air_app.models import QuestionAndAnswer
from utils import helper, textprocessing


def get_corpus(dataset, stopwords_set):
    for question, text in dataset:
        if text != '':
            tokens = textprocessing.preprocess_text(text, stopwords_set)
            print('Q: {}'.format(question))
            yield question, Counter(tokens)


def get_corpora(stopwords_set, visited_questions):
    def index_questions():
        for question in QuestionAndAnswer.objects.all():
            if question not in visited_questions:
                visited_questions.add(question)
                text = helper.extract_question_and_answer_text(question)
                yield question, text
    dataset = index_questions()

    yield from get_corpus(dataset, stopwords_set)


def index():
    stopwords_file = os.path.join(os.getcwd(), 'english-stopwords-dash.txt')
    with open(stopwords_file, mode='r', encoding='utf-8') as f:
        stopwords_set = set(f.read().split())

    questions_file = os.path.join(os.getcwd(), 'db', 'questions.db')
    lengths_file = os.path.join(os.getcwd(), 'db', 'lengths.db')
    index_db_file = os.path.join(os.getcwd(), 'db', 'index.db')
    visited_questions_file = os.path.join(os.getcwd(), 'db', 'visited_questions.db')

    visited_questions = set()
    if os.path.isfile(visited_questions_file):
        with open(visited_questions_file, mode='rb') as f:
            visited_questions = pickle.load(f)

    questions = []
    if os.path.isfile(questions_file):
        with open(questions_file, mode='rb') as f:
            questions = pickle.load(f)

    corpora = get_corpora(stopwords_set, visited_questions)

    index_db = shelve.open(index_db_file, flag='c', writeback=True)
    # Build inverted index
    helper.build_inverted_index(questions, corpora, index_db)

    # Calculate lengths for normalizing
    num_docs = len(questions)
    lengths = [0 for _ in range(num_docs)]
    for idx in range(num_docs):
        # Re-construct doc vector from inverted index
        vector = []
        for term, value in index_db.items():
            df = value['df']
            postings_list = value['postings_list']

            if idx in postings_list.keys():
                weight = helper.tf(postings_list[idx]) * helper.idf(df, num_docs)
                vector.append(weight)

        lengths[idx] = math.sqrt(sum((e ** 2 for e in vector)))

    index_db.close()

    with open(visited_questions_file, mode='wb') as f:
        pickle.dump(visited_questions, f)
    with open(questions_file, mode='wb') as f:
        pickle.dump(questions, f)
    with open(lengths_file, mode='wb') as f:
        pickle.dump(lengths, f)
