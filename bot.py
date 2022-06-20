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
                     f"Привет, {message.from_user.first_name}! Это бот ответов и вариантов ОГЭ. Что я умею 👇",
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
               "(300₽ или 700₽)\n</b></i>\n💚<i>СберБанк:</i>\n 5469550044621032\n\n 🔐<i>Bitcoin-кошелек:</i>\n" \
               "1PVMa4P8hJp3BPQo1ow3c9iNc5YvxGLf5f\n\n<i>❗<b>ВНИМАНИЕ!" + \
               "</b> В комментариях к платежу необходимо указать свой <b>индивидуальный номер</b>, " + \
               "который вы можете найти во вкладке <b>«Мой статус»</b> (кнопка «Мой статус»). <b>Платежи " + \
               "без указания ИН игнорируются!</b></i><i><b>\n\n3) Отправьте боту " \
               "скрин платежа без лишнего текста\n\n4) " + \
               "В течение часа (большая загруженность) вам будет выслано приглашение в VIP-канал и дополнительная " + \
               "информация</b>\n\nПо вопросам оплаты и любым неточностям обращаться к @ruotveti_m</i>"
        bot.send_message(call.message.chat.id, text, parse_mode='html')
    if call.data == "status":
        if vip == 0:
            vip_status = 'не активирован❌'
        elif vip == 1:
            vip_status = 'Тариф Базовый✅'
        elif vip == 2:
            vip_status = 'Тариф Премиум✅\nВаш личный куратор: @ruotveti_m'
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
    if message.chat.id == 1069991824 and str(message.text[0:6]).isdigit() and len(message.text) >= 8:
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
            # print(callback)

            vip = int(init_key(int(key))['vip'])
            # print(1)
            # print('vip', vip)

            if vip == 1 or vip == 2:
                con = sqlite3.connect("users.db")
                cur = con.cursor()
                result = cur.execute("""SELECT * FROM links""").fetchall()
                con.commit()
                con.close()
                link = ''
                for i in range(100):
                    if result[i][2] == 0:
                        link = result[i][1]
                        con = sqlite3.connect("users.db")
                        cur = con.cursor()
                        cur.execute("""UPDATE links SET used = 1 WHERE id = (?)""", (i+1,))
                        con.commit()
                        con.close()
                        break
                bot.send_message(chat_id,
                                 f"Администратор рассмотрел вашу заявку на вступление в VIP. Ваш "
                                 f"статус VIP - {'базовый' if vip == 1 else 'премиум. Ваш куратор - @ruotveti_m'}.\nС"
                                 f"сылка на вступление в VIP-канал - {link}")
                if vip == 2:
                    username = init_key(int(key))['username']
                    name = init_key(int(key))['first_name']
                    last_name = init_key(int(key))['last_name']
                    bot.send_message(960785716, f"Обновлен список премиум-аккаунтов. Новый пользователь👇\nuserna"
                                                f"me - {username}\nname - {name}\nlast_name - {last_name}\nНапиши "
                                                f"'Пользователи', чтобы получить полный список премиум-аккаунтов")
            else:
                bot.send_message(chat_id,
                                 f"Администратор рассмотрел вашу заявку на вступление в VIP. Ваш статус VIP - не "
                                 f"активирован❌. Комментарий - {comment}")
        except Exception as E:
            print(E)
    elif message.text == 'Пользователи':
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users""").fetchall()
        con.commit()
        con.close()
        # print(result)
        prem_keys = []
        for i in result:
            if i[5] == 2:
                prem_keys.append(i[4])
        # print(prem_keys)
        bot.send_message(960785716, f'Список всех премиум аккаунтов:')
        for i in range(len(prem_keys)):
            key = prem_keys[i]
            username = init_key(int(key))['username']
            name = init_key(int(key))['first_name']
            last_name = init_key(int(key))['last_name']
            bot.send_message(960785716, f"Пользователь {i+1}👇\nusername - {username}\nname - {name}\nlast_name "
                                        f"- {last_name}\nkey - {key}\n\n")

    else:
        start(message)


print('Бот запущен.')
# links = ['https://t.me/+ommYhekjD9EwMjUx', 'https://t.me/+c1_sg-G-BmhiNjIx', 'https://t.me/+S5xw7AXrIAU4NzMx',
#          'https://t.me/+1tt2xzWIu6lkNTAx', 'https://t.me/+OnbPrbMP1b4wNzkx', 'https://t.me/+9fY3hTc7DTIyYjIx',
#          'https://t.me/+UKEnnBdCsKAxMjNh', 'https://t.me/+8rm_-My2Q5I4NzRh', 'https://t.me/+r70cKwZf1ckyZGYx',
#          'https://t.me/+G9T7sUyglStlYzgx', 'https://t.me/+u7HXfRQW2llkYjAx', 'https://t.me/+JYPmOVI1_QFhMWJh',
#          'https://t.me/+p8HbON6krzk1OWYx', 'https://t.me/+mU-LOLuqKfE1NDUx', 'https://t.me/+R9dNEFa8zK8yYmYx',
#          'https://t.me/+2h6ifYYYw7g3ZGMx', 'https://t.me/+L36REqXLqHVhNDcx', 'https://t.me/+YL3h_vf7Lbc5MDNh',
#          'https://t.me/+B4EICuGXBJIxZTQx', 'https://t.me/+DXk3HKpPdh8wMjY5', 'https://t.me/+Kb1BvQGDEQRmZmZh',
#          'https://t.me/+Sm2VZKLe16M1MDUx', 'https://t.me/+2j-NAX_C6pFjZDNh', 'https://t.me/+cB-ql5qsYbZhY2Zh',
#          'https://t.me/+_i3QjIrapj4zYmVh', 'https://t.me/+LYS68E_zac5mMmQx', 'https://t.me/+PGKwUFp97eA2Njc5',
#          'https://t.me/+UNEKw9AFldBjNDAx', 'https://t.me/+AAHfxi447RRkOWUx', 'https://t.me/+s8R309RyOs1hNTUx',
#          'https://t.me/+vY1ZFjUYlkkxNDgx', 'https://t.me/+RPUvstzvNbljNjY5', 'https://t.me/+j71mMh0-gmgwZDkx',
#          'https://t.me/+XsFTOeKa-OhiZWJh', 'https://t.me/+_E8C77SMOY42NDNh', 'https://t.me/+LunP8GrzrUs5NmQx',
#          'https://t.me/+WJ2AVPz1x1U4OTUx', 'https://t.me/+GGF5VyT6z2QzODcx', 'https://t.me/+oVbSmIbjLYFmNTQx',
#          'https://t.me/+90hli1tp2awyYTIx', 'https://t.me/+ZYvVe454BRE3YzYx', 'https://t.me/+o8d-1Qv_AkM5MDAx',
#          'https://t.me/+U6TVoGPOQv45Y2Jh', 'https://t.me/+5LIqbezNXNYwZTAx', 'https://t.me/+zWdXk_Scmq4wZjNh',
#          'https://t.me/+BrjlD8SSY0E0MWU5', 'https://t.me/+l594s-6Uc-0xYjBh', 'https://t.me/+aws8L9n42QM5YWYx',
#          'https://t.me/+6lWpRcsnY8s0MTEx', 'https://t.me/+DiAthRAgm8g0M2I', 'https://t.me/+IK9MoBk1NP45N2Mx',
#          'https://t.me/+MwAPa3fjesU4ZmJh', 'https://t.me/+pYp-H6zyNpI0OGUx', 'https://t.me/+kMKQlgm_fa81MTEx',
#          'https://t.me/+hVJz3tVD3JA4OThh', 'https://t.me/+MQJtniFc625mNzhh', 'https://t.me/+DGXbsv3eJLA3YWEx',
#          'https://t.me/+t52i1lzsPw00M2Ux', 'https://t.me/+2u9ha5FG-ik4NjY5', 'https://t.me/+aR2qfXdICyw0N2Qx',
#          'https://t.me/+Gky5BepLDsE2NGNh', 'https://t.me/+JEwhGa0J_hcwN2Ex', 'https://t.me/+qQZ3aDPMtZY4MDVh',
#          'https://t.me/+Vo5zNMvqmuRlZjVh', 'https://t.me/+J5HP-t69LoE4Mjcx', 'https://t.me/+-3AjqrHUEQIxZjEx',
#          'https://t.me/+-Y5q81yzsOk1NDYx', 'https://t.me/+U6CHL8ly12JjYzAx', 'https://t.me/+9-3d3_X-ABYzYTRh',
#          'https://t.me/+qv0TV8aFuIU3NmJh', 'https://t.me/+1VgTYxFHFsU5MTAx', 'https://t.me/+ZY1GoE1JD0tjYWMx',
#          'https://t.me/+OF0AGOnTYEFmYmYx', 'https://t.me/+vBZdaH5WWVdhZjFh', 'https://t.me/+qQO4vlNpX3Y4YjVh',
#          'https://t.me/+jQ8p8FPeDQ85ZTZh', 'https://t.me/+aFq_iIYm0pAxODcx', 'https://t.me/+StiVKd6GAdBkMTEx',
#          'https://t.me/+QLKSUi7ADPU5MWUx', 'https://t.me/+58v5GLs31hg5MDcx', 'https://t.me/+T46E_kSfGVIxZDU5',
#          'https://t.me/+xScAdc9o8lY0MjYx', 'https://t.me/+vSHPf4Jxw205ZjIx', 'https://t.me/+UY04MStg344xNWJh',
#          'https://t.me/+5VhzUeeg2gM2MTFh', 'https://t.me/+I0aPVp0U1eBlNjFh', 'https://t.me/+y1p6_5c-1Y9mN2Q5',
#          'https://t.me/+5MsqV8JFNPg2MzAx', 'https://t.me/+y6022Wb1d0pmMTYx', 'https://t.me/+a_Q-paGkkMliNmIx',
#          'https://t.me/+b13Nfg2G21dmYjZh', 'https://t.me/+XTL5Q5XVFSE3NjE5', 'https://t.me/+4OcE0B47fV0zZDFh',
#          'https://t.me/+rSE9H70GvbIxYTkx', 'https://t.me/+lMqqDWFEYTtiNDk5', 'https://t.me/+usuW0cbjGWllYmMx',
#          'https://t.me/+_M2rFvDkOfk1ZTAx', 'https://t.me/+DJd40sfydxM1MzIx', 'https://t.me/+y7ktOUmnXegwZTcx',
#          'https://t.me/+e6F6GnzecC8xODlh']
#
# con = sqlite3.connect("users.db")
# cur = con.cursor()
# for i in range(len(links)):
#     sqlite_insert_query = f"""INSERT INTO links
#                          (link)
#                          VALUES
#                          ('{links[i]}')"""
#     print(sqlite_insert_query)
#     count = cur.execute(sqlite_insert_query)
# con.commit()
# con.close()

try:
    bot.infinity_polling(timeout=100, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=100, long_polling_timeout=5)
