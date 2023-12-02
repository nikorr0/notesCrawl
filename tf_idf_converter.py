# Это делает Игнат
#
# На вход подается словарь из нормализованных текстов или словарь из одного запроса (слова разделены пробелом)
# На выход возвращается словарь со списками из чисел
#
# Пример 1 (запрос):
# Вход: {0: "Хочу узнать, где можно восстановить пропуск."}
# Выход: {0: [0.9, 0. , 0. , 0. , 0.1]}
#
# Пример 2 (текст):
# Вход: {0: "кабинет соцгум восстановлениe пропуск", 2: "восстановить отчисление прийти кабинет 999"}
# Выход: {0: [0.8, 0. , 0. , 0. , 0.2], 2: [0.66666667, 0. , 0. , 0. , 0.66666667]}
#
# Ссылка на гугл колаб файл с примером реализации tf-idf (мой): 
# https://colab.research.google.com/drive/12lf77dL1nvCl5pk9TPKHDQnOSbsnZm8C?usp=sharing
#
# Ссылка на гугл колаб файл с примером реализации tf-idf (преподавателя):
# https://colab.research.google.com/drive/17Z4p0k67j4LOkpzAK1jEPw6RGW860_Lb?usp=sharing
#
# Подача и возвращение словаря нужно для того, чтобы в итоге (после поиска заметок) вывоводить самые подходящие исходные заметки по их индексам.
# Подача запроса в виде словаря сделана, чтобы в одну и ту же функцию можно было подать и запрос, и тексты (можно просто if сделать и не подавать словарь при запросе)

from sklearn.feature_extraction.text import TfidfVectorizer

# testDataset = [
#     "кабинет соцгум восстановить пропуск",
#     "восстановить отчисление прийти кабинет 999",
#     "приказ отчисление университет 92"
# ]

def getTFIDFWidthFromNotes(normalayzQuery, normalazeNotes):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(normalazeNotes)
    tfidf_query = tfidf_vectorizer.transform([normalayzQuery])
    tfidf_notes = tfidf_vectorizer.transform(normalazeNotes)
    
    return {
        "query": tfidf_query.toarray(), 
        "notes": tfidf_notes.toarray()
    }

# queryAndNotesTFIDF = getTFIDFWidthFromNotes("соцгум университет",testDataset)
# print(queryAndNotesTFIDF)
