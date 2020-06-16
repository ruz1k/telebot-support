import telebot
import schedule
import time
import random
import mysql.connector
from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

#connection with mysql
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="*****",
    password="****",
    port="3306",
    database="test"
)

cursor = mydb.cursor()

@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {}, Я Support Bot".format(user))


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(random.randint(10,20))


# this block asks question to the user
def question_message():
    msg = bot.send_message(id, "Не спишь?")
    sql = "INSERT INTO user_date SET request=NOW()"
    cursor.execute(sql)
    mydb.commit()
    bot.register_next_step_handler(msg, answer_message)


# in this block user gives answer for the question message
def answer_message(message):
    try:
        i = cursor.lastrowid
        #update mysql base
        sql = "UPDATE user_date SET response = NOW() WHERE id = %s"
        val = (i)
        cursor.execute(sql, (val,))
        mydb.commit()
        bot.send_message(id, "Хорошо!")
    except Exception as e:
        bot.reply_to(message, 'Ошибка!')


if __name__ == "__main__":
    #in this block bot sends message
    i = 0
    for i in range(1):
        delay = random.randrange(1, 12)
        schedule.every(delay).seconds.do(question_message)

    Thread(target=schedule_checker).start()

bot.polling()