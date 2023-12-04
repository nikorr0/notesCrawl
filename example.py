from text_normalization import *
from topic_selector import *
from tf_idf_converter import *
from search_texts import *

# так заметки должны хранится в файле
text_notes = "В ER моделировании нужно оставить в первом столбце только первичный ключ. \n" \
            + "310 кабинет соцгум, для восстановления пропуска.\n" + "Купить имбирное печенье к Новому году"

# каждая заметка должна быть в своей строке
raw_notes = text_notes.split("\n")

query = "Где я могу восстановить пропуск?"

# нумерация заметок
notes = dict()
for i, j in enumerate(raw_notes):
    notes[i] = j

# на вход функции nomalize() подается либо запрос в текстовом формате и режим 'query'
# либо просто словарь пронумерованных заметок
norm_query = nomalize(query, mode='query') # нормализация запроса
norm_notes = nomalize(notes) # нормализация заметок
print(norm_query) # мочь восстановить пропуск
print(norm_notes) # {0: 'er моделирование нужно оставить первый столбец первичный ключ',
                  #  1: 'кабинет соцгум восстановление пропуск', 2: 'купить имбирный печение новый год'}

# поиск заметок по темам
# на вход функции get_texts_group() подается нормализованный запрос, нормализованные заметки,
# а также количество тем, которые будут выделены у заметок и максимальное количество заметок,
# которые вернуться, если пройдут ограничение (limit)
# по умолчанию (texts_to_return=-1) максимальное количество заметок, которые могут вернуться
# состовляет в три раза меньше, чем было подано в функцию
grouped_notes = get_texts_group(norm_query, norm_notes, number_of_topics=10, texts_to_return=-1, limit=0.5)
print(grouped_notes) # {1: 'кабинет соцгум восстановление пропуск'}
 
# преобразование нормализованного запроса и группированных заметок в tf-idf
tf_idf = getTFIDFWidthFromNotes(norm_query, grouped_notes)
print(tf_idf) # {'query': array([[0., 0., 1., 0.]]), 'notes': {1: array([0.5, 0.5, 0.5, 0.5])}}
# поиск самых подходяших заметок по tf-idf запроса и заметок
ids_d = getRelevantNotesByTFIDF(tf_idf)
print(ids_d) # [{'relevated': 0.5, 'notes': 1}]

ids = list(map(lambda x: x['notes'], ids_d))
for i, j in enumerate(ids):
    print(f"{i+1}. " + notes[j])
# 1. 310 кабинет соцгум, для восстановления пропуска.
