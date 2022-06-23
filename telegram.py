import time

import telebot
import config
import app
from telebot import types
import app

bot = telebot.TeleBot(config.TOKEN)

state = "default"
question_state = 0
questions = ["Ваше имя?", "На какой адрес желаете заказать?", "Ваш номер телефона для связи?",
             "Комментарий к заказу:", "Что оставите в залог: паспорт или 100$?", "Что добавить в чашу?"]
keys = ["name", "address", "phone", "comment", "deposit", "order_el", "messenger"]
keys_on_rus = ["Имя", "Адрес", "Номер телефона", "Коментарий", "Залог", "Заказ"]
order = dict()


def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заказать ✅")
    item2 = types.KeyboardButton("Посмотреть товары 📦")

    markup.add(item1, item2)
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
    global question_state
    if state == "default":
        print(state)
        if message.chat.type == 'private':
            if message.text == 'Заказать ✅':
                state = "ordering"
                order = dict()
                question_state = 0
                bot.send_message(message.chat.id, questions[question_state], reply_markup=types.ReplyKeyboardRemove())

            elif message.text == 'Посмотреть товары 📦':
                products = app.set_products_into_telegram()
                message_products = ''
                k = 1
                for el in products:
                    message_products += str(k) + ") " + el.name
                    k += 1
                bot.send_message(message.chat.id,
                                 'У нас широкий выбор ассортимента:\n\n' + message_products + '\n\nСкорее нажми кнопку "Заказать ✅"')
            elif message.text.startswith("1)"):
                msg = message.text.split("\n")
                if len(msg) == 8:
                    bot.send_message(message.chat.id, 'Ваш заказ:\n' + message.text)
                else:
                    bot.send_message(message.chat.id, 'Извините( Я не понял ваш заказ😢')
            else:
                bot.send_message(message.chat.id, 'Я тебя немного не понял, попробуй написать /help')
    else:
        order[keys[question_state]] = message.text
        question_state += 1
        if question_state < len(questions):
            # Залог
            if question_state == 4:
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Паспорт 📕", callback_data="паспорт")
                item2 = types.InlineKeyboardButton("100$ 💵", callback_data="100$")
                markup.add(item1, item2)
                bot.send_message(message.chat.id, questions[question_state], reply_markup=markup)

            else:
                bot.send_message(message.chat.id, questions[question_state])
        else:
            message_for_user = "Пожалуйста, подтвердите заказ:\n\n"
            order[keys[len(keys) - 1]] = "@" + message.chat.username
            for i in range(0, len(keys_on_rus)):
                message_for_user += keys_on_rus[i] + ": " + order[keys[i]] + "\n"
            state = "default"

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Подтвердить ✅", callback_data="confirm")
            item2 = types.InlineKeyboardButton("Отменить ❌", callback_data="cancel")

            markup.add(item1, item2)

            bot.send_message(message.chat.id, message_for_user, reply_markup=markup)
            print(message.chat)
        print(order)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global question_state
    try:
        if call.message:
            if call.data == "паспорт" or call.data == "100$":
                order[keys[question_state]] = call.data
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text, reply_markup=None)
                bot.send_message(call.message.chat.id, "В залог будет оставлен: " + call.data)

                question_state += 1

                products = app.set_products_into_telegram()
                items = []
                for el in products:
                    items.append(types.InlineKeyboardButton(el.name, callback_data=el.id))
                markup = types.InlineKeyboardMarkup(row_width=len(items))
                markup.add(*items)
                bot.send_message(call.message.chat.id, questions[question_state], reply_markup=markup)

            elif call.data == "confirm":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text, reply_markup=None)
                if app.add_order_from_telegram(order):
                    bot.send_message(call.message.chat.id,
                                     "Ваш заказ успешно сформирован. В ближайшее время с Вами свяжется наш менеджер.",
                                     reply_markup=create_keyboard())
                else:
                    bot.send_message(call.message.chat.id,
                                     "Извините, при оформлении заказа произошла ошибка. Повторите попытку заказа немного позже.",
                                     reply_markup=create_keyboard())

            elif call.data == "cancel":
                bot.send_message(call.message.chat.id,
                                 "Начните все заново!")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
