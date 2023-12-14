# На вход подаются словарь со c tf-idf запроса и заметок
# На выход возвращается список из словарей (словарь для каждой заметки), в котором храниться релевантность и id заметки
#
# Пример:
# Вход: {"query": array([[0. , 0. , 0. , 0.70710678]]), "notes": {0: array([0.18569534, 0.18569534, 0.37139068, 0.18569534])}}
# Выход: [{'relevated': 0.7071067811865476, 'notes': 0}]
#
# Ссылка на гугл колаб файл с примером реализации tf-idf (мой): 
# https://colab.research.google.com/drive/12lf77dL1nvCl5pk9TPKHDQnOSbsnZm8C?usp=sharing

def getRelevantNotesByTFIDF (TFIDF, count = 5, delete_unrelevant=True) :
    queryTFIDF = TFIDF['query'][0]
    notesDistTFIDF = TFIDF['notes']

    relevantNotes = []
    for (key, noteTFIDF) in notesDistTFIDF.items():
        amountRelevantWords = 0.0
        for j in range(len(noteTFIDF)) :
            amountRelevantWords += noteTFIDF[j] * queryTFIDF[j]
        relevantNotes.append({
            "relevanted": amountRelevantWords,
            "id": key
        })
    
    relevantNotes.sort(reverse=True,key=lambda note:note["relevanted"])

    # Удаление записей с нулевой релевантностью
    if delete_unrelevant:
        only_relevantNotes = [relevantNotes[i] for i in range(len(relevantNotes)) if relevantNotes[i]["relevanted"] > 0]
        if len(only_relevantNotes) > 0:
            relevantNotes = only_relevantNotes

    if (len(relevantNotes) > count):
        relevantNotes = relevantNotes[:count]

    return relevantNotes
