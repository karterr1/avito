import pymorphy3
morph = pymorphy3.MorphAnalyzer()

text = "Как мне с помощью библиотеки pymorphy2 разделить строку на слова"

# разделяем строку на слова
words = text.split()

# список для хранения обработанных слов
processed_words = []

# проходим по каждому слову и обрабатываем его
for word in words:
    parsed_word = morph.parse(word)[0]

    # исключаем служебные части речи
    if 'NOUN' in parsed_word.tag or 'ADJF' in parsed_word.tag or 'VERB' in parsed_word.tag:
        # приводим слово к именительному падежу
        processed_word = parsed_word.inflect({'nomn'}).word

        processed_words.append(processed_word)

# объединяем обработанные слова в строку
result = ' '.join(processed_words)

print(result)