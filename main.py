import schedule
import time
import random
import mysql.connector
from threading import Thread
import telebot
from telebot import types

bot = telebot.TeleBot('***')

i = 0
id = **

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# this block asks question to the user
def question_message():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_net = types.KeyboardButton(text="/Net")
    keyboard.add(button_net)
    mydb = mysql.connector.connect(
    host="localhost",
    user="bet2u_db",
    password="2V6e5R8g",
    port="3306",
    database="test"
    )
    cursor = mydb.cursor()
    msg = bot.send_message(id, "Ti, ne spish?", reply_markup=keyboard)
    sql = "INSERT INTO maksBot SET request=NOW()"
    cursor.execute(sql)
    mydb.commit()
    global i
    i = cursor.lastrowid
    mydb.close()
    bot.register_next_step_handler(msg, answer_message)

# in this block user gives answer for the question message
@bot.message_handler(commands=["Net"])
def answer_message(message):
    try:
        global i
        mydb = mysql.connector.connect(
            host="localhost",
            user="bet2u_db",
            password="2V6e5R8g",
            port="3306",
            database="test"
            )
        cursor = mydb.cursor()
        #update mysql base
        sql = "UPDATE `maksBot` SET `response`= CASE WHEN `response` = '0000-00-00 00:00:00' THEN NOW() ELSE `response` END WHERE `id` = %s"
        val = (i)
        cursor.execute(sql, (val,))
        mydb.commit()
        bot.send_message(id, "Horosho!")
    except Exception as e:
        bot.send_message(id, 'Error\n{}'.format(e))


if __name__ == "__main__":
    j = 0
    for j in range(1):
        schedule.every(6).to(10).hours.do(question_message)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True)
