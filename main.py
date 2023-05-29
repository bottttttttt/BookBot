import re

import telebot
from telebot import types
import sqlite3 as sq
import config
import markups as nav

bot = telebot.TeleBot(config.TOKEN)
db = 'LIB.db'
conn = sq.connect(db)
reader_num = None #переменная для ввода читательского билета
Name = None
Title = None
title_add= None
autor_f= None
autor_i= None
date = None
genre = None
description = None

autor_name = None
autor_surname = None
autor_date = None
autor_id = None
autor_birth = None
autor_death = None

@bot.message_handler(commands=['add'])
def autor_add(message):
    bot.send_message(message.chat.id, "Введите имя")


@bot.message_handler(commands=['autor'])
def autor_test(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM autor')
    autor_test = cur.fetchall()

    info = ''
    for el in autor_test:
        info += f'{el[0]}) {el[1]} {el[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🔑 Авторизация')
    btn2 = types.KeyboardButton('🔍 Поиск')
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)
    #bot.register_next_step_handler(message, on_click)

@bot.message_handler(content_types=['text'])
def on_click(message):
    if message.text == '🔑 Авторизация':
        bot.send_message(message.chat.id, '✏️ Введите номер читательского билета')
        bot.register_next_step_handler(message, login_1)

    elif message.text == '🔍 Поиск':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🔍 Автора по [имени фамилии]')
        markup.add(btn1)
        btn2 = types.KeyboardButton('🔍 Книги по названию')
        btn3 = types.KeyboardButton('🔍 Книги по жанрам')
        markup.add(btn2, btn3)
        back = types.KeyboardButton("↩️ Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="уточните плиз", reply_markup=markup)
        bot.register_next_step_handler(message, search)

    elif (message.text == "↩️ Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("🔑 Авторизация")
        button2 = types.KeyboardButton("🔍 Поиск")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="👾 На такую комманду я не запрограммирован..")
@bot.message_handler(content_types=['text'])
def search(message):
    if message.text == '🔍 Книги по жанрам':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('роман', callback_data='роман')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('детектив', callback_data='детектив')
        markup.row(btn2)
        btn3 = types.InlineKeyboardButton('антиутопия', callback_data='антиутопия')
        markup.row(btn3)
        bot.send_message(message.chat.id,'Выберите жанр 🤓', reply_markup=markup)
        #bot.register_next_step_handler(message, genre)
    elif message.text == '🔍 Книги по названию':
        bot.send_message(message.chat.id, 'Введите название ')
        bot.register_next_step_handler(message, search_title)

    elif message.text == '🔍 Автора по [имени фамилии]':
        bot.send_message(message.chat.id, 'Введите фамилию автора')
        bot.register_next_step_handler(message, search_autor_name)

    elif (message.text == "↩️ назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton('🔍 По названию')
        btn3 = types.KeyboardButton('🔍 По жанрам')
        markup.add(btn2, btn3)
    else:
        bot.send_message(message.chat.id, text="👾 На такую комманду я не запрограммирован..")

@bot.message_handler(content_types=['text'])
def search_autor_name(message):
    global autor_f
    autor_f = message.text
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    cur.execute("SELECT autor_f FROM autor WHERE autor_f = ?", (autor_f,))
    autor= cur.fetchall()
    if (not bool(len(autor))):
        bot.send_message(message.chat.id, '🤷 Такого автора нет в нашей библиотеке')
    else:
        bot.register_next_step_handler(message, search_autor)
        bot.send_message(message.chat.id, 'Введите имя автора')
    cur.close()
    conn.close()
def search_autor(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    global autor_i
    global autor_f
    autor_i = message.text
    cur.execute("SELECT autor_id FROM autor WHERE autor_i = ?", (autor_i,))
    autor = cur.fetchall()
    if (not bool(len(autor))):
        bot.send_message(message.chat.id, '🤷 Такого автора нет в нашей библиотеке')
    else:
        global autor_id
        bot.send_message(message.chat.id, f'1 {autor_id}')
        for el in autor:
            autor_id = f'{el[0]}'
        #autor_id1 = str(autor)
        #autor_id = autor_id1.replace("[('", '')
        #autor_id = autor_id.replace("',)]", '')
        bot.send_message(message.chat.id, f'2 {autor_id}')

        markup = types.InlineKeyboardMarkup()
        btn1 = types.KeyboardButton('ℹ️ Об авторе')
        markup.add(types.InlineKeyboardButton('ℹ️ Об авторе', callback_data='ℹ️ Об авторе'))
        bot.send_message(message.chat.id, f'Автор {autor_i} {autor_f} есть в нашей библиотеке', reply_markup=markup)
        #bot.register_next_step_handler(message, search_title_2)
    cur.close()
    conn.close()

@bot.message_handler(content_types=['text'])
def search_title(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    global Title
    Title = message.text
    cur.execute("SELECT title FROM book WHERE title = ?", (Title,))
    title_1 = cur.fetchall()
    if (not bool(len(title_1))):
        bot.send_message(message.chat.id, '🤷 Книга не найдена')
    else: #вывод книг
        markup = types.InlineKeyboardMarkup()
        btn1 = types.KeyboardButton('ℹ️ О книге')
        markup.add(types.InlineKeyboardButton('ℹ️ О книге', callback_data='ℹ️ О книге'))
        global Name
        bot.send_message(message.chat.id, f'Книга с названием "{Title}" есть в нашей библиотеке', reply_markup=markup)
        #bot.register_next_step_handler(message, search_title_2)
    cur.close()
    conn.close()

#@bot.message_handler(content_types=['text'])


@bot.callback_query_handler(func=lambda callback: True)
def mega_search(callback):
    if callback.data == 'ℹ️ Об авторе':
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        global autor_id

        cur.execute("SELECT autor_death FROM autor WHERE autor_id = ?", (autor_id,))
        death = cur.fetchall()
        for el in death:
            death_info = {el[0]}
        cur.execute("SELECT * FROM autor WHERE autor_id = ?", (autor_id,))
        autor = cur.fetchall()
        autor_info = ''
        bot.send_message(callback.message.chat.id, f'3 {death_info}')
        for el in autor:
            if (death_info=={None}): #это ужас, а не условие...
                autor_info = f'{el[1]} {el[2]}\nДата рождения: {el[3]}'
            else:
                autor_info = f'{el[1]} {el[2]}\nДаты жизни: {el[3]} - {el[4]}'
        bot.send_message(callback.message.chat.id, autor_info)
        cur.close()
        conn.close()

    elif (callback.data =='роман')or(callback.data == 'детектив')or(callback.data == 'антиутопия'):
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        genre = callback.data
        bot.send_message(callback.message.chat.id, f'Все книги жанра {callback.data}:')
        cur.execute("SELECT title, autor_f, autor_i, date FROM book WHERE genre = ?", (callback.data,))
        book = cur.fetchall()
        book_info = ''
        for el in book:
            book_info += f'{el[0]}\nАвтор: {el[1]} {el[2]}\nДата публикации: {el[3]}\n-- -- --\n'
        bot.send_message(callback.message.chat.id, book_info)
        cur.close()
        conn.close()

    elif callback.data == 'ℹ️ О книге':
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        global Title
        bot.send_message(callback.message.chat.id, Title)
        cur.execute("SELECT autor_f, autor_i, date, genre, description FROM book WHERE title = ?", (Title,))
        book = cur.fetchall()
        book_info = ''
        for el in book:
            book_info += f'Автор: {el[0]} {el[1]}\nДата публикации: {el[2]}\nЖанр: {el[3]}\n ...\n{el[4]}\n'
        bot.send_message(callback.message.chat.id, book_info)
        cur.close()
        conn.close()

    elif (callback.data =='роман')or(callback.data == 'детектив')or(callback.data == 'антиутопия'):
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        genre = callback.data
        bot.send_message(callback.message.chat.id, f'Все книги жанра {callback.data}:')
        cur.execute("SELECT title, autor_f, autor_i, date FROM book WHERE genre = ?", (callback.data,))
        book = cur.fetchall()
        book_info = ''
        for el in book:
            book_info += f'{el[0]}\nАвтор: {el[1]} {el[2]}\nДата публикации: {el[3]}\n-- -- --\n'
        bot.send_message(callback.message.chat.id, book_info)
        cur.close()
        conn.close()



#@bot.message_handler(content_types=['text'])
def login_1(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    global reader_num
    reader_num = message.text
    # cur.execute("SELECT name FROM user WHERE reader_num = 123")
    cur.execute("SELECT name FROM user WHERE reader_num = ?", (reader_num,))
    global Name
    Name = cur.fetchall()
    if (not bool(len(Name))):
        bot.send_message(message.chat.id, '🤷 Читатель не найден')
    else:
        #bot.send_message(message.chat.id, Name)
        bot.send_message(message.chat.id, 'Введите пароль ')
        bot.register_next_step_handler(message, login_2)


def login_2(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    global reader_num
    password = message.text
    # cur.execute("SELECT name FROM user WHERE reader_num = 123")
    cur.execute("SELECT password FROM user WHERE reader_num = ?", (reader_num,))
    login_2 = cur.fetchall()
    #Пытаемся отфарматировать полученный пароль для проверки
    password_1 = str(login_2)
    res_pass = password_1.replace("[('", '')
    res_pass = res_pass.replace("',)]", '')
    #танцы с бубном

    if (reader_num=='0')and(res_pass == password):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn0 = types.KeyboardButton('👤 Список читателей')
        markup.add(btn0)
        btn1 = types.KeyboardButton('Добавить книгу 📚')
        btn2 = types.KeyboardButton('🗑 Удалить книгу 📚')
        markup.add(btn1, btn2)
        btn3 = types.KeyboardButton('Добавить автора ✍️')
        btn4 = types.KeyboardButton('🗑 Удалить автора ✍️')
        markup.add(btn3, btn4)
        back = types.KeyboardButton("↩️ Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, 'Вход с правами администратора', reply_markup=markup)
        bot.register_next_step_handler(message, admin)

    elif res_pass == password:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('📚 Список моих книг')
        markup.add(btn1)
        back = types.KeyboardButton("↩️ Вернуться в главное меню")
        markup.add(back)
        global Name
        Name_new = str(Name)
        Name_new_new = Name_new.replace("[('", '')
        Name_new_new = Name_new_new.replace("',)]", '')
        bot.send_message(message.chat.id, f'С возвращением, {Name_new_new}!', reply_markup=markup)
        bot.register_next_step_handler(message, my_list)
    else:
        bot.send_message(message.chat.id, '❌ Пароль не верен')


def admin(message):
    if message.text == '👤 Список читателей':
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        #bot.send_message(message.chat.id, 'Список ваших книг с датами возврата: ')
        cur.execute("SELECT * FROM user")
        my_list = cur.fetchall()
        list_info = ''
        for el in my_list:
            list_info += f'{el[0]}) {el[3]} {el[4]}\nНомер читательского билета: {el[1]}\nПароль: {el[2]}\n...\n'
        bot.send_message(message.chat.id, list_info)
        cur.close()
        conn.close()
        bot.register_next_step_handler(message, admin)

    elif message.text == 'Добавить автора ✍️':
        bot.send_message(message.chat.id, 'Введите фамилию автора для добавления')
        bot.register_next_step_handler(message, addautor_f)

    elif message.text == '🗑 Удалить автора ✍️':
        bot.send_message(message.chat.id, 'Введите фамилию автора для удаления')
        bot.register_next_step_handler(message, delete_autor_f)

    elif message.text =='Добавить книгу 📚':
        bot.send_message(message.chat.id, 'Введите название книги')
        bot.register_next_step_handler(message, addbook_title)

    elif message.text =='🗑 Удалить книгу 📚':
        bot.send_message(message.chat.id, 'Введите название книги для удаления')
        bot.register_next_step_handler(message, delete)

def delete_autor_f(message):
    global autor_f
    autor_f = message.text.strip()
    bot.send_message(message.chat.id, 'Введите имя автора')
    bot.register_next_step_handler(message, delete_autor)
def delete_autor(message):
    global autor_i
    global autor_f
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    autor_i = message.text.strip()
    cur.execute(f"SELECT autor_f FROM autor WHERE (autor_f = '{autor_f}') AND (autor_i = '{autor_i}')")
    autor = cur.fetchall()
    if (not bool(len(autor))):
        bot.send_message(message.chat.id, '🤷 Автор не найден')
    else:
        cur.execute(f"DELETE FROM autor WHERE (autor_f = '{autor_f}') AND (autor_i = '{autor_i}')")
        conn.commit
        bot.send_message(message.chat.id, '✅ Автор удален')
    cur.close()
    conn.close()

def addautor_f(message):
    global autor_f
    autor_f = message.text.strip()
    bot.send_message(message.chat.id, 'Введите имя автора')
    bot.register_next_step_handler(message, addautor_i)

def addautor_i(message):
    global autor_i
    autor_i = message.text.strip()
    bot.send_message(message.chat.id, 'Введите год рождения автора')
    bot.register_next_step_handler(message, addautor_birth)

def addautor_birth(message):
    global autor_birth
    autor_birth = message.text.strip()
    bot.send_message(message.chat.id, 'Введите год смерти автора, если есть\nЕсли нет - напишите "нет"')
    bot.register_next_step_handler(message, addautor)

def addautor(message):
    death = message.text.strip()
    global autor_death
    if death != 'нет':
        autor_death = death
    global autor_f
    global autor_i
    global autor_birth

    conn = sq.connect('LIB.db')
    cur = conn.cursor()

    if death != 'нет':
        autor_death = death
        cur.execute(f"INSERT INTO autor ("
                    f"autor_i, autor_f, autor_birth, autor_death"
                    f") VALUES ('%s','%s','%s','%s'"
                    f")" % (autor_i, autor_f, autor_birth, autor_death))
        conn.commit()
    else:
        cur.execute(f"INSERT INTO autor ("
                    f"autor_i, autor_f, autor_birth"
                    f") VALUES ('%s','%s','%s'"
                    f")" % (autor_i, autor_f, autor_birth))
        conn.commit()

    bot.send_message(message.chat.id, "Добавленно:")
    cur.execute("SELECT * FROM autor WHERE autor_f = ?", (autor_f,))
    autor = cur.fetchall()
    autor_info = ''
    for el in autor:
        if death != 'нет':
            autor_info += f'{el[1]} {el[2]}\nДаты жизни: {el[3]} - {el[4]}\n'
        else:
            autor_info += f'{el[1]} {el[2]}\nДата рождения: {el[3]}\n'
    bot.send_message(message.chat.id, autor_info)
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, admin)

def delete(message):
    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    book_del = message.text.strip()
    cur.execute("SELECT title FROM book WHERE title = ?", (book_del,))
    title_1 = cur.fetchall()
    if (not bool(len(title_1))):
        bot.send_message(message.chat.id, '🤷 Книга не найдена')
    else:  # вывод книг
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM book WHERE title = '{book_del}'")
        conn.commit
        bot.send_message(message.chat.id, '✅ Книга удалена')
    cur.close()
    conn.close()

def addbook_title(message):
    global title_add
    title_add = message.text.strip()
    bot.send_message(message.chat.id, 'Введите фамилию автора')
    bot.register_next_step_handler(message, addbook_f)

def addbook_f(message):
    global autor_f
    autor_f = message.text.strip()
    bot.send_message(message.chat.id, 'Введите имя автора')
    bot.register_next_step_handler(message, addbook_i)

def addbook_i(message):
    global autor_i
    autor_i = message.text.strip()
    bot.send_message(message.chat.id, 'Введите дату публикации')
    bot.register_next_step_handler(message, addbook_date)

def addbook_date(message):
    global date
    date = message.text.strip()
    bot.send_message(message.chat.id, 'Введите жанр книги')
    bot.register_next_step_handler(message, addbook_genre)

def addbook_genre(message):
    global genre
    genre = message.text.strip()
    bot.send_message(message.chat.id, 'Введите описание книги')
    bot.register_next_step_handler(message, addbook)

def addbook(message):
    global description
    description = message.text.strip()
    global genre
    global date
    global autor_i
    global autor_f
    global title_add

    conn = sq.connect('LIB.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO book ("
                f"autor_f, autor_i, title, date, genre, description"
                f") VALUES ('%s','%s','%s','%s','%s','%s'"
                f")" % (autor_f, autor_i, title_add, date, genre, description))
    conn.commit()

    bot.send_message(message.chat.id, "Добавленно:")
    cur.execute("SELECT title, autor_f, autor_i, genre, date, description FROM book WHERE title = ?", (title_add,))
    book = cur.fetchall()
    book_info = ''
    for el in book:
        book_info += f'{el[0]}\nАвтор: {el[1]} {el[2]}\nЖанр: {el[3]}\nДата публикации: {el[4]}\n-- -- --\n{el[5]}\n'
    bot.send_message(message.chat.id, book_info)
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, admin)

@bot.message_handler(content_types=['text'])
def my_list(message):
    if message.text == '📚 Список моих книг':
        conn = sq.connect('LIB.db')
        cur = conn.cursor()
        global reader_num
        bot.send_message(message.chat.id, 'Список ваших книг с датами возврата: ')
        cur.execute("SELECT title, date_in, date_out FROM list WHERE reader_num =?", (reader_num,))
        my_list = cur.fetchall()
        list_info = ''
        for el in my_list:
            list_info += f'{el[1]} - {el[2]} || {el[0]} \n'
        bot.send_message(message.chat.id, list_info)
        cur.close()
        conn.close()
    elif (message.text == "↩️ Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("🔑 Авторизация")
        button2 = types.KeyboardButton("🔍 Поиск")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="👾 На такую комманду я не запрограммирован..")

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower()== 'id':
        bot.reply_to(message, f'ID:  {message.from_user.id}')


bot.infinity_polling()
#bot.polling(none_stop=True)