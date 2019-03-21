# -*- coding: utf-8 -*-
import config
import telebot
import time
import datetime
import os

script_dir = os.path.dirname(__file__)
bot = telebot.TeleBot(config.token)


# Словарь сложных лексем
class GlueWordDictionary:
    f_name = ''  # Имя файла со словарём
    g_words = {}  # Словарь вида Сложная лексема - склеенная в одно слово сложная лексема

    def __init__(self, file_name):
        self.f_name = file_name
        f = open(self.f_name, 'r', encoding="utf8")
        for line in f:
            not_glue = ''
            glue = ''
            for item in line.split()[1:]:
                    not_glue += ' ' + item
                    glue += '_' + item
            self.g_words[not_glue[1:]] = glue[1:]


PartOfSpeech = {
    'СУ': 'Существительное',
    'ПП': 'Полное прилагательное',
    'КП': 'Краткое прилагательное',
    'ДЕ': 'Деепричастие',
    'ГЛ': 'Глагол',
    'НП': 'Неопределённое'}


class FlexiesDictionary:
    f_name = ''
    f_words = {}

    def __init__(self, file_name):
        self.f_name = file_name
        f = open(self.f_name, 'r', encoding="utf8")

        while True:
            line = f.readline()
            if not line:
                break
            self.f_words[line.split()[1]] = []  # Потом надо заполнить морфологическую информацию
            for x in range(line.split()[2]):
                f.readline()


class CharactersDictionary:
    f_name = ''
    c_words = {}
    quaziBase = ''
    canonicForm = ''
    wordType = PartOfSpeech['НП']
    wordChanging = -1

    def __init__(self, file_name):
        self.f_name = file_name
        f = open(self.f_name, 'r', encoding="urf8")

        for line in f:
            split_line = line.split()
            self.quaziBase = split_line[1]
            self.canonicForm = split_line[2]
            self.wordType = PartOfSpeech[split_line[3]]
            self.wordChanging = split_line[4]


ch_dictionary = CharactersDictionary(os.path.join(script_dir, '../Dictionaries/Characters.dct'))
gw_dictionary = GlueWordDictionary(os.path.join(script_dir, '../Dictionaries/GluedWords.dct'))
greetings = ('hi', 'hello')


def today_greetings(hour):
    if 6 <= hour < 12:
        return 'Good morning, '
    elif 12 <= hour < 17:
        return 'Good day, '
    elif 17 <= hour < 23:
        return 'Good evening, '

def morphology(word):

    return word


# Функция обрабатывает любой текст, который пришёл
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text.lower() in greetings:
        bot.send_message(message.chat.id, today_greetings(datetime.datetime.now().hour)+message.from_user.first_name)
    else:
        input_str = message.text.upper()  # Переводим входную фразу в верхний регистр
        # Склеиваем сложные лексемы
        for gw in gw_dictionary.g_words:
            if gw in input_str:
                input_str = input_str.replace(gw, gw_dictionary.g_words[gw])
        # Разбиваем входную строку на слова
        words = input_str.split()
        # Формируем ответ
        output = ''
        for word in words:
            output += word + '\n'
        # Отправляем ответ
        bot.send_message(message.chat.id, output)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)
