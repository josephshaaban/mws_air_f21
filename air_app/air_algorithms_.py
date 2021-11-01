import nltk
from nltk.corpus import stopwords, LazyCorpusLoader, WordListCorpusReader
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import glob
import re
import os
import numpy as np
import sys

from air_app.models import QuestionAndAnswer


# see https://medium.com/voice-tech-podcast/information-retrieval-using-boolean-query-in-python-e0ea9bf57f76
stopwords_ = LazyCorpusLoader(
    "stopwords", WordListCorpusReader, r"(?!README|\.).*", encoding="utf8"
)
Stopwords = set(stopwords_.words('english'))


def finding_all_unique_words_and_freq(words):
    words_unique = set(words)
    word_freq = {}

    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq


def finding_freq_of_word_in_doc(word, words):
    freq = words.count(word)


def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex, '', text)
    return text_returned


class Node:
    def __init__(self, docId, freq=None):
        self.freq = freq
        self.doc = docId
        self.nextval = None


class SlinkedList:
    def __init__(self, head=None):
        self.head = head


def boolean_model(query):
    dict_global = {}

    questions_with_pk = {}
    questions_and_answers = QuestionAndAnswer.objects.all()

    for q_a in questions_and_answers:
        print(q_a)
        q = q_a.question_text
        a = q_a.answer_text
        text = f'{q}\n{a}'
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'), '', text)
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word for word in words if len(words) > 1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        dict_global.update(finding_all_unique_words_and_freq(words))
        questions_with_pk[q_a.pk] = os.path.basename(q_a.question_text)

    unique_words_all = set(dict_global.keys())

    linked_list_data = {}
    for word in unique_words_all:
        linked_list_data[word] = SlinkedList()
        linked_list_data[word].head = Node(1, Node)

    for q_a in questions_and_answers:
        q = q_a.question_text
        a = q_a.answer_text
        text = f'{q}\n{a}'
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'), '', text)
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word for word in words if len(words) > 1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        word_freq_in_doc = finding_all_unique_words_and_freq(words)
        for word in word_freq_in_doc.keys():
            linked_list = linked_list_data[word].head
            while linked_list.nextval is not None:
                linked_list = linked_list.nextval
            linked_list.nextval = Node(q_a.pk, word_freq_in_doc[word])

    query = word_tokenize(query)
    connecting_words = []

    different_words = []
    for word in query:
        if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
            different_words.append(word.lower())
        else:
            connecting_words.append(word.lower())
    print(connecting_words)
    total_files = len(questions_with_pk)
    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []
    for word in different_words:
        if word.lower() in unique_words_all:
            zeroes_and_ones = [0] * total_files
            linkedlist = linked_list_data[word].head
            print(word)
            while linkedlist.nextval is not None:
                zeroes_and_ones[linkedlist.nextval.doc - 1] = 1
                linkedlist = linkedlist.nextval
            zeroes_and_ones_of_all_words.append(zeroes_and_ones)
        else:
            print(word, " not found")
            sys.exit()
    print(zeroes_and_ones_of_all_words)
    for word in connecting_words:
        word_list1 = zeroes_and_ones_of_all_words[0]
        word_list2 = zeroes_and_ones_of_all_words[1]
        if word == "and":
            bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, word_list2)]
            zeroes_and_ones_of_all_words.remove(word_list1)
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.insert(0, bitwise_op)
        elif word == "or":
            bitwise_op = [w1 | w2 for (w1, w2) in zip(word_list1, word_list2)]
            zeroes_and_ones_of_all_words.remove(word_list1)
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.insert(0, bitwise_op)
        elif word == "not":
            bitwise_op = [not w1 for w1 in word_list2]
            bitwise_op = [int(b == True) for b in bitwise_op]
            zeroes_and_ones_of_all_words.remove(word_list2)
            zeroes_and_ones_of_all_words.remove(word_list1)
            bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, bitwise_op)]
    zeroes_and_ones_of_all_words.insert(0, bitwise_op)

    questions = []
    print(zeroes_and_ones_of_all_words)
    lis = zeroes_and_ones_of_all_words[0]
    for index in lis:
        if index == 1:
            questions.append(questions_with_pk[cnt])
        cnt = cnt + 1
    return questions


