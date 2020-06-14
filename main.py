import telebot
import schedule
import datetime
import time
import random
import mysql.connector
from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

#connection with mysql
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    port="3306",
    database="telebot"
)

cursor = mydb.cursor()
# create database in mysql
# cursor.execute("CREATE DATEBASE telebot")
# drop and create table commands in mysql
# cursor.execute("DROP TABLE user_date")
# cursor.execute("CREATE TABLE user_date (date_otpravki TIME, date_otveta TIME)")

@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {}, Я Support Bot".format(user))


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(random.randint(1,10))


# this block asks question to the user
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


# in this block user gives answer for the question messag3
def answer_message(message):
    try:
        date = datetime.datetime.now().time()
        q = date.strftime("%H:%M:%S")
        #update mysql base
        sql = "UPDATE user_date SET date_otveta = %s"
        val = (q)
        cursor.execute(sql, (val,))
        mydb.commit()
        bot.send_message(id, "Хорошо!")
    except Exception as e:
        bot.reply_to(message, 'oops')


if __name__ == "__main__":
    #in this block bot sends message
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).seconds.do(question_message)

    Thread(target=schedule_checker).start()

bot.polling()