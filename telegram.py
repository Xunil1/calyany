import telebot
import config

from telebot import types


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заказать ✅")
    item2 = types.KeyboardButton("Посмотреть товары 📦")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать! Я бот по заказу кальянов на дом. Благодаря мне ты можешь с легкостью забронировать кальян на нужное тебе время!",
                     parse_mode='html',
                     reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вижу тебе нужна моя помощь!\nПопробуй начать сначала.\nДля этого нажми кнопку "Заказать ✅"')


@bot.message_handler(content_types=['text'])
def main_send(message):
    if message.chat.type == 'private':
        if message.text == 'Заказать ✅':
            bot.send_message(message.chat.id, 'Для офрмления заказа укажите в одном сообщении:\n1) Имя\n2) Номер телефона\n3) Дата\n4) Время\n5) Адрес\n6) На сколько времени хотите арендовать\n7) Какой табак желаете\n8) Комментарий к заказу\n\nПример:\n1) Рустам\n2) +79999999999\n3) 01.01.2022\n4) 19:00\n5) ул.Пушкина, д.10, кв.10\n6) 2 часа\n7) DarkSide хвойный, DarkSide зеленый чай\n8) Перед приездом позвонить, во дворе шлагбаум')
        elif message.text == 'Посмотреть товары 📦':
            products = "1) DarkSide хвойный\n2) DarkSide зеленый чай"
            bot.send_message(message.chat.id, 'У нас широкий выбор ассортимента:\n\n' + products + '\n\nСкорее нажми кнопку "Заказать ✅"')
        elif message.text.startswith("1)"):
            msg = message.text.split("\n")
            if len(msg) == 8:
                bot.send_message(message.chat.id, 'Ваш заказ:\n' + message.text)
            else:
                bot.send_message(message.chat.id, 'Извините( Я не понял ваш заказ😢')
        else:
            bot.send_message(message.chat.id, 'Я тебя немного не понял, попробуй написать /help')




bot.polling(none_stop=True)