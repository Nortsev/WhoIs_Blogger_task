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


def load_news():
    data = datetime.datetime.now()
    period = datetime.datetime.now() - datetime.timedelta(days=30)
    headings = []
    googlenews = GoogleNews(lang='en', region='US')
    googlenews.set_time_range(data.strftime('%m/%d/%Y'), period.strftime('%m/%d/%Y'))
    googlenews.search('Russia')
    googlenews.results()
    i = 1
    while googlenews.page_at(i):
        title = googlenews.page_at(i)
        for titles in title:
            headings.append(titles['title'])
        print(f'Скачивание {i} страницы завершенно')
        i += 1
        time.sleep(7)

    return headings


def exclude_stop_words(txt_blob):
    regexp = re.compile('[^a-zA-Z-]+')
    usable_words = {}
    stops = stopwords.words('english')
    for item in txt_blob.word_counts.items():
        if regexp.search(item[0]):
            continue

        lemmatized_word = Word(item[0].lower()).lemmatize()
        if lemmatized_word not in stops:
            if lemmatized_word not in usable_words:
                usable_words[lemmatized_word] = item[1]
            else:
                usable_words[lemmatized_word] = usable_words[lemmatized_word] + item[1]
    return usable_words


def generate_wc(words, mask_image, file_name, max_count=50):
    # Import mask image for word cloud
    mask_image = imageio.imread(mask_image)
    wordcloud = WordCloud(width=1000, height=1000,
                          colormap='prism', mask=mask_image, background_color='write')
    wc = wordcloud.fit_words({item[0]: item[1] for item in words[:max_count]})
    wc.to_file(file_name)
    plt.figure(figsize=(10, 10))
    plt.axis("off")
    plt.imshow(wc, cmap=plt.cm.gray)


def main():
    blob_txt = TextBlob(''.join(load_news()))
    usable_words = exclude_stop_words(blob_txt).items()
    sorted_words = sorted(usable_words, key=itemgetter(1), reverse=True)
    generate_wc(sorted_words, 'russia.png', 'out.png', 50)


if __name__ == '__main__':
    main()
