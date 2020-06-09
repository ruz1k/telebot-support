import telebot
import schedule
import datetime
import time
import random
from random import randint

from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {}, Я Support Bot".format(user))

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(120)

def message_func():
    date = datetime.datetime.now()
    info = bot.send_message(id, "Не спишь? {}".format(date))

def register_to_db(message):
    with open('support.txt', 'w') as out:
        out.write(str(message.from_user.first_name) + ' is ' + datetime.datetime.now() + '\n')

if __name__ == "__main__":
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).minutes.do(message_func)

    Thread(target=schedule_checker).start()

bot.polling()