import time

import telebot
import config
from telebot import types
import app



global order
bot = telebot.TeleBot(config.TOKEN)

state = "default"
questions = {
    "name": "Ваше имя?",
    "address": "На какой адрес желаете заказать?",
    "phone": "Ваш номер телефона для связи?",
    "comment": "Комментарий к заказу:",
    "deposit": "Что оставите в залог: паспорт или 100$?",
    "order_el": ["Что добавить в чашу?", "Хотите добавить в чашу что-то еще?"]
    }

keys = ["name", "address", "phone", "comment", "deposit", "order_el", "order_price", "messenger"]
keys_on_rus = {
    "name": "Имя",
    "address": "Адрес",
    "phone": "Номер телефона",
    "comment": "Коментарий",
    "deposit": "Залог",
    "order_el": "Заказ"
    }

order_price = 0


def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заказать ✅")
    item2 = types.KeyboardButton("Посмотреть товары 📦")

    markup.add(item1, item2)
    return markup


def create_keyboard_products():
    products = app.set_products_into_telegram()
    items = []
    for el in products:
        items.append(types.InlineKeyboardButton(el.name, callback_data=el.name))
    markup = types.InlineKeyboardMarkup(row_width=4)
    markup.add(*items)
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать! Я бот по заказу кальянов на дом. Благодаря мне ты можешь с легкостью забронировать кальян на нужное тебе время!",
                     parse_mode='html',
                     reply_markup=create_keyboard())


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'Вижу тебе нужна моя помощь!\nПопробуй начать сначала.\nДля этого нажми кнопку "Заказать ✅"')


@bot.message_handler(content_types=['text'])
def main_send(message):
    global state
    global order
    global order_price
    if state == "default":
        if message.chat.type == 'private':
            if message.text == 'Заказать ✅':
                state = "ordering"
                order = {
                    "name": "",
                    "address": "",
                    "phone": "",
                    "comment": "",
                    "deposit": "",
                    "order_el": [],
                    "messenger": "",
                    "order_price": 30
                }
                order["messenger"] = "@" + message.chat.username
                order_price = 0
                bot.send_message(message.chat.id, questions["name"], reply_markup=types.ReplyKeyboardRemove())

            elif message.text == 'Посмотреть товары 📦':
                products = app.set_products_into_telegram()
                message_products = ''
                k = 1
                for el in products:
                    message_products += str(k) + ") " + el.name + "\n"
                    k += 1
                bot.send_message(message.chat.id,
                                 'У нас широкий выбор ассортимента:\n\n' + message_products + '\nСкорее нажми кнопку "Заказать ✅"')
            else:
                bot.send_message(message.chat.id, 'Я тебя немного не понял, попробуй написать /help')
    else:
        if order["name"] == "":
            order["name"] = message.text
            bot.send_message(message.chat.id, questions["address"])
        elif order["address"] == "":
            order["address"] = message.text
            bot.send_message(message.chat.id, questions["phone"])
        elif order["phone"] == "":
            order["phone"] = message.text
            bot.send_message(message.chat.id, questions["comment"])
        elif order["comment"] == "":
            order["comment"] = message.text
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Паспорт 📕", callback_data="паспорт")
            item2 = types.InlineKeyboardButton("100$ 💵", callback_data="100$")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, questions["deposit"], reply_markup=markup)
        elif order["deposit"] == "":
            if message.text in ["паспорт", "100$"]:
                order["deposit"] = message.text
                bot.send_message(message.chat.id, questions["order_el"][0], reply_markup=create_keyboard_products())
            else:
                bot.send_message(message.chat.id, "Для лучшего взаимодействия воспользуйтесь кнопками под сообщением)")
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Паспорт 📕", callback_data="паспорт")
                item2 = types.InlineKeyboardButton("100$ 💵", callback_data="100$")
                markup.add(item1, item2)
                bot.send_message(message.chat.id, questions["deposit"], reply_markup=markup)
        elif state == "make_choice":
            bot.send_message(message.chat.id, "Для лучшего взаимодействия воспользуйтесь кнопками под сообщением)")
            bot.send_message(message.chat.id, questions["order_el"][0], reply_markup=create_keyboard_products())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global state
    products = app.set_products_into_telegram()
    products_list = []
    for el in products:
        products_list.append(el.name)
    try:
        if call.message:
            if call.data == "паспорт" or call.data == "100$":
                order["deposit"] = call.data
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
                bot.send_message(call.message.chat.id, "В залог будет оставлен: " + call.data)
                bot.send_message(call.message.chat.id, questions["order_el"][0], reply_markup=create_keyboard_products())
                state = "make_choice"

            elif call.data in products_list:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data + " добавлена в чашу.", reply_markup=None)

                flag = True
                for el in order["order_el"]:
                    if call.data == el[:-3]:
                        order["order_el"][order["order_el"].index(el)] = el[:-1] + str(int(el[-1]) + 1)
                        flag = False
                if flag:
                    order["order_el"].append(call.data + " x1")

                item1 = types.InlineKeyboardButton("Да", callback_data="yes")
                item2 = types.InlineKeyboardButton("Нет", callback_data="no")
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, questions["order_el"][1], reply_markup=markup)

            elif call.data == "yes" or call.data == "no":
                if call.data == "yes":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Добавим еще.", reply_markup=None)
                    bot.send_message(call.message.chat.id, questions["order_el"][0], reply_markup=create_keyboard_products())
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично, тогда скорее переходим к подтверждению заказа)", reply_markup=None)
                    message_for_user = "Пожалуйста, подтвердите заказ:\n\n"

                    for el in keys_on_rus:
                        if el != "order_el":
                            message_for_user += keys_on_rus[el] + ": " + order[el] + "\n"

                    order_message = ''
                    for_order = ''
                    for el in order["order_el"]:
                        order_message += "     " + el + "\n"
                        for_order += el + "; "

                    order["order_el"] = for_order

                    message_for_user += keys_on_rus["order_el"] + ": \n" + order_message + "\n"

                    state = "default"

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("Подтвердить ✅", callback_data="confirm")
                    item2 = types.InlineKeyboardButton("Отменить ❌", callback_data="cancel")

                    markup.add(item1, item2)

                    bot.send_message(call.message.chat.id, message_for_user, reply_markup=markup)
            elif call.data == "confirm" or call.data == "cancel":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
                if call.data == "confirm":
                    if app.add_order_from_telegram(order):
                        bot.send_message(call.message.chat.id, "Ваш заказ успешно сформирован. В ближайшее время с Вами свяжется наш менеджер.", reply_markup=create_keyboard())
                    else:
                        bot.send_message(call.message.chat.id, "Извините, при оформлении заказа произошла ошибка. Повторите попытку заказа немного позже.", reply_markup=create_keyboard())
                else:
                    bot.send_message(call.message.chat.id, "Начните все заново!", reply_markup=create_keyboard())
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)