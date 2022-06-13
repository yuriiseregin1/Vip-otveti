import random

import telebot
import sqlite3
from telebot import types
from telegram import *
from telegram.ext import *
from requests import *
from aiogram import Bot, Dispatcher, executor, types
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
import shutil
import os

bot = telebot.TeleBot("5450119210:AAEQCpv-4gnS4pA6esF66SRzdgA0wg3wL1Y")


def get_result():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM users""").fetchall()
    con.commit()
    con.close()
    return result


def init_key(key):
    result = get_result()
    callback = None
    for i in result:
        if i[4] == key:
            callback = {
                'username': i[1],
                'first_name': i[2],
                'last_name': i[3],
                'vip': i[5],
                'chat_id': i[6]
            }

    return callback


def init(message):
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.from_user.id
    register = False
    result = get_result()
    for i in result:
        if chat_id == i[6]:
            id = i[0]
            key = i[4]
            vip = i[5]
            register = True
    if not register:
        vip = 0
        key = random.randint(100000, 999999)
        keys = []
        for i in result:
            keys.append(i[4])
        while key in keys:
            key = random.randint(100000, 999999)
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        sqlite_insert_query = f"""INSERT INTO users
                             (username, first_name, last_name, key, chat_id)
                             VALUES
                             ('{username}', '{first_name}', '{last_name}', {key}, {chat_id});"""
        a = "INSERT INTO users (username, first_name, last_name, key, chat_id) VALUES (?, ?, ?)"
        count = cur.execute(sqlite_insert_query)
        con.commit()
        con.close()
    else:
        for i in result:
            if i[1] == username:
                chat_id = i[6]
    callback = {'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'key': key,
                'vip': vip,
                'chat_id': chat_id}
    return callback


@bot.message_handler(commands=['start'])
def start(message):
    callback = init(message)
    username, first_name, last_name, key, vip, chat_id = callback['username'], callback['first_name'], \
                                                         callback['last_name'], callback['key'], callback['vip'], \
                                                         callback['chat_id']

    keyboard = types.InlineKeyboardMarkup()

    button_join_VIP = types.InlineKeyboardButton(text='Вступить в VIP', callback_data='join_VIP')
    keyboard.add(button_join_VIP)

    button_status = types.InlineKeyboardButton(text='Мой статус', callback_data='status')
    keyboard.add(button_status)

    button_about_VIP = types.InlineKeyboardButton(text='Что такое VIP', callback_data='about_VIP')
    keyboard.add(button_about_VIP)

    button_conditions = types.InlineKeyboardButton(text='Условия покупки', callback_data='conditions')
    keyboard.add(button_conditions)

    button_questions = types.InlineKeyboardButton(text='Частые вопросы', callback_data='questions')
    keyboard.add(button_questions)

    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Это бот сливов ответов и вариантов ОГЭ. Что я умею 👇",
                     reply_markup=[keyboard])
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    register = False
    result = get_result()
    for i in result:
        if chat_id == i[6]:
            id = i[0]
            key = i[4]
            vip = i[5]
            register = True
    if not register:
        vip = 0
        key = random.randint(100000, 999999)
        keys = []
        for i in result:
            keys.append(i[4])
        while key in keys:
            key = random.randint(100000, 999999)
        print(f"{username}: {message.text}")
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        sqlite_insert_query = f"""INSERT INTO users
                             (username, first_name, last_name, key, chat_id)
                             VALUES
                             ('{username}', '{first_name}', '{last_name}', {key}, {chat_id});"""
        count = cur.execute(sqlite_insert_query)
        con.commit()
        con.close()
    else:
        print(f"{username}: {message.text}")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    callback = init(message=call)
    username, first_name, last_name, key, vip, chat_id = callback['username'], callback['first_name'], \
                                                         callback['last_name'], callback['key'], callback['vip'], \
                                                         callback['chat_id']
    if call.data == "join_VIP":
        text = "<i><b>Как приобрести VIP доступ?</b></i>\n\n 1) <i><b>Выберите тариф VIP</b></i>\n🪙Базовый - <b>" + \
               "300₽</b> <s>900₽</s>\n🔑Премиум - <b>700₽</b> <s>1500₽</s>\n\n2) <i><b>Совершите оплату" + \
               "(300₽ или 700₽)</b></i>\n💚<i>СберБанк:</i>\n XXXX XXXX XXXX XXXX\n\n🧡<i>QIWI:</i>\n" + \
               "+7XXXXXXXXXX\n\n 🔐<i>Bitcoin-кошелек:</i>\n1PVMa4P8hJp3BPQo1ow3c9iNc5YvxGLf5f\n\n<i>❗<b>ВНИМАНИЕ!" + \
               "</b> В комментариях к платежу необходимо указать свой <b>индивидуальный номер</b>, " + \
               "который вы можете найти во вкладке <b>«Мой статус»</b> (кнопка «Мой статус»). <b>Платежи " + \
               "без указания ИН игнорируются!</b></i><i><b>\n\n3) Отправьте боту скрин платежа без лишнего текста\n\n4) " + \
               "В течение часа (большая загруженность) вам будет выслано приглашение в VIP-канал и дополнительная " + \
               "информация</b>\n\nПо вопросам оплаты и любым неточностям обращаться к @ruotveti_m</i>"
        bot.send_message(call.message.chat.id, text, parse_mode='html')
    if call.data == "status":
        if vip == 0:
            vip_status = 'не активирован❌'
        elif vip == 1:
            vip_status = 'Тариф Базовый✅'
        elif vip == 2:
            vip_status = 'Тариф Премиум✅'
        else:
            print("Значение VIP не соответствует заданным параметрам -", vip)
            vip_status = 'Обратитесь к администратору - @ruotveti_m'
        text = f"Твой статус👇\nПользователь: {username}\nИмя: {first_name}\nФамилия: {last_name}\nИндвидиульный" + \
               f" номер: {key}\nСтатус VIP: {vip_status}"
        bot.send_message(call.message.chat.id, text)
    if call.data == "about_VIP":
        img = open("vip.jpg", 'rb')
        bot.send_photo(call.message.chat.id, img)
        text = "<i>Что такое VIP?</i>\n\n 📍VIP-канал Ответы.ру - приватный канал, в котором мы публикуем абсолютно " + \
               "<u><b>все ответы на каждый экзамен ОГЭ</b></u>\n\n 🥳Приобретая VIP, вы получаете доступ в" + \
               "приватный канал <u><b>на весь учебный год!</b></u> Мы публикуем ответы для досрочного этапа сдачи " + \
               "ОГЭ, основного, а также дополнительных дней и дней пересдачи\n\n 🗒<u><b>Два VIP тарифа:</b></u>\n\n" + \
               "<i><b><u>1) Базовый тариф</u></b></i>🪙\n<i>Стоимость: <u>300₽</u> </i>(повышение 22 июня❗️)\n" + \
               "<i>В тариф входит:</i>\n✅ Доступ в VIP-канал со всеми ответами\n\n<i><b><u>2) Премиум " + \
               "тариф</u></b></i>🔑\n <i>Стоимость: <u>700₽</u></i> (повышение 22 июня❗️)\n <i>В тариф входит:</i>\n" + \
               "✅ Доступ в VIP-канал со всеми ответами\n✅ Личный онлайн-куратор (помощь, ответы на вопросы," + \
               "общение)\n✅ Эксклюзивный набор стикеров\n\n❗️<b>Обратите внимание: скоро возможно повышение цен!</b>"
        bot.send_message(call.message.chat.id, text, parse_mode='html')
    if call.data == "conditions":
        text = "\n\n<i>Условия доступа в VIP-канал Ответы.ру:</i>\n\n <b>1)</b>Покупка доступа в VIP-канал является" + \
               "<u><b> исключительно добровольной</b></u>, никто не может заставить вас принять данное решение\n\n" + \
               "<b>2)</b> <u><b>Мы не даем 100% гарантий правильности ответов!</b></u> Всегда остается вероятность " + \
               "того, что материалы, опубликованные в VIP-канале могут частично или полностью не совпасть с " + \
               "заданиями и ответами на экзамене \n\n<b>3)</b> <u><b>Возврат денежных средств после покупки " + \
               "доступа в VIP-канал не предусмотрен!</b></u> \n\n<b>4)</b> <u><b>Распространения пригласительной " + \
               "ссылки и (или) любых материалов из VIP-канала карается баном</b></u> без возврата денежных средств!" + \
               "\n\n⚠️Помните, что все, кто предлагает вам 100%-ные гарантии правильности ответов являются мошенниками!"
        bot.send_message(call.message.chat.id, text, parse_mode='html')

    if call.data == "questions":
        text = "<i><b>Частые вопросы</b></i>\n\n ❓<i>Что публикуется в VIP-канале?\n</i> В VIP-канале мы публикуем " + \
               "<u><b>полные ответы</b></u> на ОГЭ по все предметам, покупаю доступ в канал вы получаете ответы " + \
               "на весь период проведения ОГЭ (досрочный этап, основной, дополнительные дни и дни пересдачи)\n\n" + \
               "<i> ❓На какие регионы будут ответы?</i> \nОтветы публикуются в специально подготовленных " + \
               "<u><b>сборниках</b></u>, а также отдельно формируется <u><b>на каждый регион</b></u>\n\n" + \
               "<i> ❓Когда публикуются ответы? Будет ли возможность подготовиться?</i>\n Ответы в заранее " + \
               "подготовленных сборниках выкладываются <u><b>за 1-2 дня</b></u> до официальной даты проведения " + \
               "экзамена, сформированные ответы для каждого региона - <u><b>за 1-3 часа</b></u> до экзамена. Это " + \
               "отличное время для того чтобы подготовиться\n\n ❓<i>100% гарантия правильности ответов?</i>\n" + \
               "<b>Мы не даем 100%-ной гарантии правильности ответов!</b> Но мы дорожим вашим доверием, решаем " + \
               "КИМы, находим и проверяем все ответы, а отзывы наших клиентов вы можете прочитать в канале: " + \
               "@ruotveti_otz <b>Запомните: те кто предлагают вам точные ответы и 100%-ные гарантии - " + \
               "мошенники!</b>\n\n<i> ❓Чем ваш канал отличается от каналов конкурентов?</i>\n <b>Наша команда " + \
               "экспертов</b> самостоятельно прорешивает все варианты ОГЭ. Таким образом мы первыми получаем " + \
               "правильные ответы и делимся ими с участниками VIP-канала. <u><b>Чаще всего ответы в других каналах " + \
               "появляются на 30-60 минут позже чем у нас</b></u>"
        bot.send_message(call.message.chat.id, text, parse_mode='html')

    # if call.data == "check_True":
    #     bot.send_message(call.message.chat.id, "оплата принята")
    # if call.data == "check_False":
    #     bot.send_message(call.message.chat.id, "оплата отклонена")


@bot.message_handler(content_types=['photo'])
def accepting_check(message):
    callback = init(message)
    username, first_name, last_name, key, vip, chat_id = callback['username'], callback['first_name'], \
                                                         callback['last_name'], callback['key'], callback['vip'], \
                                                         callback['chat_id']

    # keyboard = types.InlineKeyboardMarkup()

    # button_x64 = types.InlineKeyboardButton(text='✅', callback_data='check_True')
    # keyboard.add(button_x64)

    # button_x32 = types.InlineKeyboardButton(text='❌', callback_data='check_False')
    # keyboard.add(button_x32)

    bot.send_message(1069991824, f'Пользователь {message.from_user.username} Отправил фото. KEY - {key}')
    bot.send_message(message.chat.id,
                     'Спасибо за фото. Оно уже отправлено администратору и находится на проверке. Как' +
                     ' только он проверит оплату, бот сразу же вышлет тебе ссылку для вступления в VIP-канал')
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = open(name, 'rb')
    bot.send_photo(1069991824, img)


@bot.message_handler(content_types=['text'])
def accepting_check(message):
    if message.chat.id == 1069991824 and len(message.text) >= 8:
        try:
            comment = ''
            if len(message.text) > 8:
                comment = message.text[8:]
            # (str(message.text)[0:6], str(message.text)[-1])
            callback = init_key(int(str(message.text)[0:6]))
            key = message.text[0:6]
            vip = str(message.text)[7]
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            req = f"UPDATE users SET vip = ({str(message.text)[7]}) WHERE key = ({str(message.text)[0:6]})"
            cur.execute(req)
            con.commit()
            chat_id = callback['chat_id']
            print(callback)

            vip = int(init_key(int(key))['vip'])
            print(1)
            print('vip', vip)
            if vip == 1 or vip == 2:
                bot.send_message(chat_id,
                                 f"Администратор рассмотрел вашу заявку на вступление в VIP. Ваш статус VIP - {'базовый' if vip == 1 else 'премиум'}")
            else:
                bot.send_message(chat_id,
                                 f"Администратор рассмотрел вашу заявку на вступление в VIP. Ваш статус VIP - не активирован❌. Комментарий - {comment}")
        except Exception as E:
            print(E)
    start(message)


print('Бот запущен.')
try:
    bot.infinity_polling(timeout=100, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=100, long_polling_timeout=5)
