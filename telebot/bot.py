# -*- coding: utf-8 -*-
import config
import telebot
import time
import  datetime

bot = telebot.TeleBot(config.token)
greetings = ('hi', 'hello')


def today_greetings(hour):
    if 6 <= hour < 12:
        return 'Good morning, '
    elif 12 <= hour < 17:
        return 'Good day, '
    elif 17 <= hour < 23:
        return 'Good evening, '


@bot.message_handler(content_types=["text"]) #Функция обрабатывает любой текст, который пришёл
def repeat_all_messages(message):
    if message.text.lower() in greetings:
        bot.send_message(message.chat.id, today_greetings(datetime.datetime.now().hour)+message.from_user.first_name)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print (e)
            time.sleep(15)
