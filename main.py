import telebot
import sqlite3

from telebot import types

bot = telebot.TeleBot('5894373501:AAFu4VUBNTgHZR8mCABWCvhlLxbv5qfClX0')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>\nДля того, чтобы занять место в учебке, необходимо:\n1)прочитать  правила /rules\n2)нажать /takespot\nЕсли что-то непонятно /help'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['rules'])
def start(message):
    mess = f'Правила учебки:надо чо то тут'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['count'])
def start(message):
    connect = sqlite3.connect('spots.db')
    cursor = connect.cursor()
    cursor.execute("SELECT SUM(count) FROM users")
    count = int(cursor.fetchone()[0])
    connect.commit()
    mess = f'Количество свободных мест -  {50 - count}'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['takespot'])
def choosespot(message):
    connect = sqlite3.connect('spots.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER, count INTEGER)""")
    connect.commit()
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        users_list = [message.chat.id, 1]
        cursor.execute("INSERT INTO users VALUES(?, ?);", users_list)
        cursor.execute("SELECT SUM(count) FROM users")
        count = int(cursor.fetchone()[0])
        connect.commit()
        if count < 50:
            mess = f'Вы заняли место в учебной комнате, приятной работы!^_^\nПосле окончания работы в учебке, просьба освободить место, нажав на кнопку releasespot в меню бота'
        else:
            mess = f'К сожалению, в данный момент все места заняты'
    else:
        mess = 'Вы уже заняли место'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    cursor.close()
    connect.close()

@bot.message_handler(commands=['releasespot'])
def releasespot(message):
    connect = sqlite3.connect('spots.db')
    cursor = connect.cursor()
    users_delete = f"""DELETE from users where id = {message.chat.id}"""
    cursor.execute(users_delete)
    connect.commit()
    cursor.close()
    connect.close()
    mess = 'Вы освободили место, спасибо!'
    bot.send_message(message.chat.id, mess, parse_mode='html')
# кнопка
@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить веб сайт", "https://www.youtube.com/"))
    bot.send_message(message.chat.id, '', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    mess = '/start - старт бота\n/takespot - занять место\n/releasespot - освободить место(обязательно)\n/count - количество свободных мест\n/rules - правила учебки'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start = types.KeyboardButton('/start')
    takespot = types.KeyboardButton('/takespot')
    rules = types.KeyboardButton('/rules')
    count = types.KeyboardButton('/count')
    delete = types.KeyboardButton('/releasespot')
    markup.add(start,takespot,delete,rules,count)



@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Я Динара':
        bot.send_message(message.chat.id, 'Динара САЛАМ!', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Не понял', parse_mode='html')


bot.polling(none_stop=True)
