import telebot
import schedule
import datetime
import time
import random
import mysql.connector

from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    port="3306",
    database="telebot"
)

# cursor = mydb.cursor()
#cursor.execute("CREATE DATEBASE telebot")
#cursor.execute("CREATE TABLE user_date (date_otpravki TIME, date_otveta TIME)")
# cursor.execute("SHOW TABLES")
# for x in cursor:
#      print(x)
# sql = "INSERT INTO user_date (date_otpravki, date_otveta) VALUES (%s, %s)"
# val = (datetime.datetime.now().time(), datetime.datetime.now().time())
# cursor.execute(sql, val)
# mydb.commit()

#cursor.execute("ALTER TABLE user_date ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

class User:
    def __init__(self):
        self.ot_date = ''
        self.date = ''

@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {}, Я Support Bot".format(user))

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(random.randint(10,100))


def message_func():
    date = datetime.datetime.now()
    msg = bot.send_message(id, "Не спишь? {}".format(date))
    msg_time = msg.datetime.datetime.now().time()
    bot.register_next_step_handler(msg, otvet_msg)
    return msg

def ot_msg(message):
    try:
        user.ot_date = msg_time
    except Exception as e:
        bot.reply_to(message,'oops')

def otvet_msg(message):
     try:
         user.date = datetime.datetime.now()
     except Exception as e:
         bot.reply_to(message, 'oops')

if __name__ == "__main__":
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).hours.do(message_func)

    Thread(target=schedule_checker).start()

bot.polling()