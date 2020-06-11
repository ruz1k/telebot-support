import telebot
import schedule
import datetime
import time
import random
import mysql.connector

from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     passwd="root",
#     port="3307",
# )
#
# print(mydb)
#
# user_data = {}

# cursor = mydb.cursor()
#
# cursor.execute("CREATE DATABASE telebot")

class User:
    def __init__(self, ot_date):
        self.ot_date = ot_date
        self.date = ''

@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {}, Я Support Bot".format(user))

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(.01)


def message_func():
    date = datetime.datetime.now()
    msg = bot.send_message(id, "Не спишь? {}".format(date))
    bot.register_next_step_handler(msg, msg_func)
    return msg

def msg_func(message):
    try:
        user_id = message.from_user.id
        user_data[user_id]=User(datetime.datetime.now())
    except Exception as e:
        bot.reply_to(message,'oops')

def otvet_msg(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.date = message.date

if __name__ == "__main__":
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).seconds.do(message_func)

    Thread(target=schedule_checker).start()

bot.polling()