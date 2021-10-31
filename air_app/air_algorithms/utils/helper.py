from collections import defaultdict
import math


def tf(freq):
    return 1 + math.log(freq)


def idf(df, num_docs):
    return math.log(num_docs / df)


def build_inverted_index(questions, corpora, index_db):
    for question, bow in corpora:
        questions.append(question)
        index = len(questions) - 1

        for term, freq in bow.items():
            if index_db.get(term, None) is None:
                index_db[term] = {}

            if index_db[term].get('df', None) is None:
                index_db[term]['df'] = 0

            if index_db[term].get('postings_list', None) is None:
                index_db[term]['postings_list'] = {}

            index_db[term]['df'] += 1
            index_db[term]['postings_list'][index] = freq

            index_db.sync()

        index_db.sync()


def extract_question_and_answer_text(q_n_a_obj):
    return f'{q_n_a_obj.question_text}\n{q_n_a_obj.answer_text}'
