from datetime import datetime, timedelta
from flask import Flask
import random
import re
import os

cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
words_from_book = []
count_sessions = 0

app = Flask(__name__)


# Task 1
@app.route('/')
def hello():
    return 'Привет, мир!'


# Task 2
@app.route('/cars')
def viewing_list():
    for i in range(len(cars)):
        yield "{} ".format(cars[i])


# Task 3
@app.route('/cats')
def random_word():
    return random.choice(cats)


# Task 4
@app.route('/time')
def time():
    return "Точное время: {:%H:%M:%S}".format(datetime.now())


# Task 5
@app.route('/correction_time')
def correction_time():
    now_time = datetime.now() + timedelta(hours=1)
    return "Точное время через час будет: {:%H:%M:%S}".format(now_time)


# Task 6
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    for i_line in book:
        words_from_book.extend(filter(None, re.split(r'\W+', i_line)))


@app.route('/word_from_book')
def word_from_book():
    return random.choice(words_from_book)


# Task 7
@app.route('/counter')
def counter():
    global count_sessions
    count_sessions += 1
    return str(count_sessions)


if __name__ == "__main__":
    app.run(debug=True)