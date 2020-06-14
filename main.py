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

user_data = {}
cursor = mydb.cursor()
# cursor.execute("CREATE DATEBASE telebot")
# cursor.execute("CREATE TABLE user_date (date_otpravki TIME, date_otveta TIME)")
# cursor.execute("DROP TABLE user_date")
# for x in cursor:
#      print(x)
# sql = "INSERT INTO user_date (date_otpravki, date_otveta) VALUES (%s, %s)"
# val = (datetime.datetime.now().time(), datetime.datetime.now().time())
# cursor.execute(sql, val)
# mydb.commit()
# cursor.execute("ALTER TABLE user_date ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

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
        time.sleep(random.randint(1,10))


def question_message():
    msg = bot.send_message(id, "Не спишь?")
    ot_date = datetime.datetime.now().time()
    x = ot_date.strftime("%H:%M:%S")
    sql = "INSERT INTO user_date (date_otpravki) \
                                      VALUES (%s)"
    val = (x)
    cursor.execute(sql, (val,))
    mydb.commit()
    bot.register_next_step_handler(msg, answer_message)


def answer_message(message):
    try:
        date = datetime.datetime.now().time()
        q = date.strftime("%H:%M:%S")
        sql = "INSERT INTO user_date (date_otveta) \
         VALUES (%s)"
        val = (q)
        cursor.execute(sql, (val,))
        mydb.commit()
        bot.send_message(id, "Хорошо!")
    except Exception as e:
        bot.reply_to(message, 'oops')


if __name__ == "__main__":
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).seconds.do(question_message)

    Thread(target=schedule_checker).start()

bot.polling()
