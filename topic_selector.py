# На вход подаются 1) нормализованный запрос 2) словарь из нормализованных текстов 
# На выход возвращается список из самых подходящих текстов, если таких текстов нет, то возвращается "None"
#
# Пример:
# Вход: 
# Нормализованный запрос: "восстановить пропуск" 
# Словарь нормализованных текстов: {0: "кабинет соцгум восстановлениe пропуск",
#                                   1: "стол дерево", 2: "восстановить отчисление прийти кабинет 999"}
#
# Выход: {0: "кабинет соцгум восстановлениe пропуск", 2: "восстановить отчисление прийти кабинет 999"}

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from scipy.spatial import distance

def get_sorted_keys(d, texts_to_return):
    sorted_values = sorted(d.values())[:texts_to_return]
    sorted_keys = list()
    for i in range(len(sorted_values)):
        for key, value in d.items():
            if value == sorted_values[i]:
                 sorted_keys.append(key)
    return sorted_keys

def get_texts_group(query, texts_dict, number_of_topics=10, texts_to_return=-1, limit=0.5):
    if texts_to_return <= 0:
      texts_to_return = len(texts_dict) // 3

    query = query.split()
    texts = [text.split() for text in texts_dict.values()]
    ids = [id for id in texts_dict.keys()]
    grouped_texts = texts_dict.copy()

    common_dictionary = Dictionary(texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in texts]
    query = common_dictionary.doc2bow(query)

    lda = LdaModel(common_corpus, num_topics=number_of_topics, minimum_probability=0.0, passes=20, iterations=20, random_state=1)

    query_probs = [value[1] for value in lda[query]]
    distances = dict()
    
    for i in ids:
        text_probs = [value[1] for value in lda[common_corpus[i]]]
        dist = distance.cosine(query_probs, text_probs)
        if dist < limit:
            distances[i] = distance.cosine(query_probs, text_probs)
    
    sorted_keys = get_sorted_keys(distances, texts_to_return)

    for id in (set(ids) - set(sorted_keys)):
        del grouped_texts[id]

    return grouped_texts