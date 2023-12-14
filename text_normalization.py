# На вход подается словарь из текстов и их номеров или словарь из одного запроса и его номера (0)
# На выход возвращается словарь из нормализованных текстов (слова разделены пробелом)
#
# Пример 1 (запрос):
# Вход: {0 : "Хочу узнать, где можно восстановить пропуск."}
# Выход: {0 : "восстановить пропуск"}
#
# Пример 2 (текст):
# Вход: {0: "310 кабинет соцгум, для восстановления пропуска.",
#        1: "Стол из дерева", 2: "Чтобы восстановиться после отчисления, нужно прийти в кабинет 999."}
# Выход: {0: "кабинет соцгум восстановлениe пропуск",
#         1: "стол дерево", 2: "восстановить отчисление прийти кабинет 999"}
#
# Подача и возвращение словаря нужно для того, чтобы в итоге (после поиска заметок) вывоводить самые подходящие исходные заметки по их индексам.
# Подача запроса в виде словаря сделана, чтобы в одну и ту же функцию можно было подать и запрос, и тексты

import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3

def nomalize(texts_dict, mode="dict_texts"):
    morph_analyzer = pymorphy3.MorphAnalyzer()
    stop_words = stopwords.words('russian')

    if mode == "query":
        if type(texts_dict) == type(str()):
            texts = [texts_dict]
        if type(texts_dict) == type(list()):
            texts = texts_dict
        if type(texts_dict) == type(dict()):
            mode="dict_texts"

    if mode != "query":
        texts = [text for text in texts_dict.values()]
        ids = [id for id in texts_dict.keys()]

    norm_texts = list()
    for text in texts:
        for p in string.punctuation:
            text = text.replace(p, ' ').strip()
        text = text.lower()
        text = re.sub('[0-9]+', '', text)
        norm_words = list()

        for word in word_tokenize(text):
            if word in stop_words:
                continue
            else:
                word = morph_analyzer.parse(word)[0].normal_form
                norm_words.append(word)
        norm_texts.append(norm_words)

    if mode == "query":
        return " ".join(norm_texts[0])

    norm_texts_dict = dict()
    for id, text in zip(ids, norm_texts):
        norm_texts_dict[id] = " ".join(text)
    
    return norm_texts_dict
