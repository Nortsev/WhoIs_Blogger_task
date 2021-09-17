"""Представим, что Вы готовите слайд для презентации об актуальных трендах в англоязычных новостях, касающихся России.

С сайта google news (https://news.google.com) (язык и регион - English | United States) необходимо
прокачать все статьи за последний месяц (на момент прокачки) с ключевым словом Russia.
Затем для скачанных статей необходимо рассчитать топ-50 упоминаемых тем и представить их в виде word (tag) cloud.

Данное задание необходимо выполнить с помощью Python.
Для представления в виде word cloud можно использовать уже существующие библиотеки.
Пример word cloud можно посмотреть по ссылке -
https://altoona.psu.edu/sites/altoona/files/success-word-cloud.jpg"""

from GoogleNews import GoogleNews
import datetime
import time
from nltk.corpus import stopwords
import re
from textblob import TextBlob, Word
from operator import itemgetter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import imageio


def load_news(period: int, key: str):
    """ Загрузка новостей
    :params int period: Период выборки новостей
    :params str key: Ключевое слово для поиска
    : return list headings: Лист с заголовками новостей за указанный период
    """

    # Получение сегодняшней даты
    data = datetime.datetime.now()
    # Задание  периода 30 дней
    period = datetime.datetime.now() - datetime.timedelta(days=period)
    # Создание  списа для хранения скаченых новостей
    headings = []
    # Передача языка и региона в библиотеку Google News
    googlenews = GoogleNews(lang='en', region='US')
    # Передача периода в в библиотеку Google News
    googlenews.set_time_range(data.strftime('%m/%d/%Y'), period.strftime('%m/%d/%Y'))
    # Передача ключевого слова для поиска
    googlenews.search(key)
    # Получение результата
    googlenews.results()
    # Создание счётчика страниц i
    i = 1
    # Создание цикла для получения данных со страниц результатов
    while googlenews.page_at(i):
        # Получение страницы с номером i
        title = googlenews.page_at(i)
        for titles in title:
            # Добавленние заголовков в список headings
            headings.append(titles['title'])
        print(f'Скачивание {i} страницы завершенно')
        i += 1
        # Приостановка программы для избежания блокировки (из-за частых запросов)
        time.sleep(7)
    print("Закачивание новостей завершенно")
    return headings


def exclude_stop_words(txt_blob: TextBlob):
    """ Обрабока полученных новостей
    :params TextBlob txt_blob: текстовый обьект TextBlob
    : return  dict usable_words: словарь слов с количтвом повторений"""

    # Определение регуляного выражения для выборки только слов
    regexp = re.compile('[^a-zA-Z-]+')
    # Создание словаря для результатов
    usable_words = {}
    # Определение словаря стоп слов
    stops = stopwords.words('english')
    # Цикл фильтрации данных
    for item in txt_blob.word_counts.items():
        # Фильтрация на основе регулярного вырыжения
        if regexp.search(item[0]):
            continue
        # Проведение лемматизации (преобразования слов в его базовую форму) данных
        lemmatized_word = Word(item[0].lower()).lemmatize()
        if lemmatized_word not in stops:
            if lemmatized_word not in usable_words:
                usable_words[lemmatized_word] = item[1]
            else:
                usable_words[lemmatized_word] = usable_words[lemmatized_word] + item[1]
    return usable_words


def generate_wc(words: list, image: str, file_name: str, max_count: int):
    """ Генерация Word Cloud
    :params list words: Отсортированный лист с зачниями слово:количество повторенний
    :params str image: Имя файла в директории для маски
    :params str file_name: Имя файла для сохранение результата
    :params int max_count: Количество слов передавоемых в Word Cloud
    : return  dict usable_words: словарь слов с количтвом повторений"""

    # Импорт изображения в Word Cloud
    image = imageio.imread(image)
    # Настройка обькта Word Cloud
    wordcloud = WordCloud(width=1000, height=1000,
                          colormap='prism', mask=image, background_color='white')
    # Выборка слов по количествку повторений и передача в Word Cloud
    wc = wordcloud.fit_words({item[0]: item[1] for item in words[:max_count]})
    # Запись результа в файл
    wc.to_file(file_name)
    plt.figure(figsize=(10, 10))
    plt.axis("off")
    plt.imshow(wc, cmap=plt.cm.gray)


def main():
    blob_txt = TextBlob(''.join(load_news(30, 'Russia')))
    print("Формирование изображение Word Cloud")
    usable_words = exclude_stop_words(blob_txt).items()
    sorted_words = sorted(usable_words, key=itemgetter(1), reverse=True)
    generate_wc(sorted_words, 'russia.png', 'result.png', 50)


if __name__ == '__main__':
    main()
