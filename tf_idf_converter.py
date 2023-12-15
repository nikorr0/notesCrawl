# На вход подается словарь из нормализованных текстов или словарь из одного запроса (слова разделены пробелом)
# На выход возвращается словарь со c tf-idf запроса и заметок
#
# Пример (запрос и текст):
# Вход: "восстановить пропуск", {0: "кабинет соцгум восстановлениe пропуск", 2: "восстановить отчисление прийти кабинет 999"}
# Выход: {"query": array([[0. , 0. , 0. , 0.70710678]]), "notes": {0: array([0.18569534, 0.18569534, 0.37139068, 0.18569534])}}
#
# Ссылка на гугл колаб файл с примером реализации tf-idf (мой): 
# https://colab.research.google.com/drive/12lf77dL1nvCl5pk9TPKHDQnOSbsnZm8C?usp=sharing
#
# Ссылка на гугл колаб файл с примером реализации tf-idf (преподавателя):
# https://colab.research.google.com/drive/17Z4p0k67j4LOkpzAK1jEPw6RGW860_Lb?usp=sharing

from sklearn.feature_extraction.text import TfidfVectorizer

def getTFIDFWidthFromNotes(normalayzQuery, normalazeNotes):
    tfidf_vectorizer = TfidfVectorizer()

    collectionNotes = [v for v in normalazeNotes.values()]
    tfidf_vectorizer.fit(collectionNotes)

    tfidf_query = tfidf_vectorizer.transform([normalayzQuery])
    
    notesTFIDF = {}
    for (keyNote, normalazeNote) in normalazeNotes.items():
        notesTFIDF[keyNote] = tfidf_vectorizer.transform([normalazeNote]).toarray()[0]

    return {
        "query": tfidf_query.toarray(), 
        "notes": notesTFIDF
    }
