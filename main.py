import telebot
import schedule
import time
import random
import mysql.connector
from threading import Thread

bot = telebot.TeleBot('1194470771:AAGDMTviS3zdweu_xmJgfOwhB7bPlG1O7DU')
id = 455257905

i = 0
@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Hello, {}, I Support Bot".format(user))


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(random.randint(5, 10))


# this block asks question to the user
def question_message():
        mydb = mysql.connector.connect(
            host="localhost",
            user="***",
            password="***",
            port="3306",
            database="test"
            )
    cursor = mydb.cursor()
    msg = bot.send_message(id, "Hi are you sleeping?")
    sql = "INSERT INTO maksBot SET request=NOW()"
    cursor.execute(sql)
    mydb.commit()
    global i
    i = cursor.lastrowid
    mydb.close()
    bot.register_next_step_handler(msg, answer_message)

# in this block user gives answer for the question message
def answer_message(message):
    try:
        global i
        print(i)
        mydb = mysql.connector.connect(
            host="localhost",
            user="***",
            password="***",
            port="3306",
            database="test"
            )
        cursor = mydb.cursor()
        #update mysql base
        sql = "UPDATE maksBot SET response = NOW() WHERE id = %s"
        val = (i)
        cursor.execute(sql, (val,))
        mydb.commit()
        bot.send_message(id, "Okay!")
    except Exception as e:
        bot.send_message(id, 'Error!')


if __name__ == "__main__":
    #in this block bot sends message
    j = 0
    for j in range(1):
        delay = random.randrange(1, 8)
        schedule.every(delay).hours.do(question_message)

    Thread(target=schedule_checker).start()

bot.polling()
