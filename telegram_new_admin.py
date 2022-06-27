import telebot
import config
import app

bot = telebot.TeleBot(config.TOKEN_ADMIN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Бот успешно запущен",
                     parse_mode='html')


def send_message(turple_order):
    file = open("id.txt", "r")
    chat_id = file.read()
    file.close()

    message = "Номер заказа: #" + str(turple_order["id"]) + "\nЗаказ: " + str(turple_order["name"])
              #"\nИмя: " + str(turple_order["name"]) + "\nТелефон: " + str(turple_order["phone"]) + "\nАдрес: " + str(turple_order["address"]) + "\nID товара: "   + str(turple_order["product_id"]) + "\nНазвание товара: " + str(turple_order["product_name"]) + "\nЦена товара: " + str(turple_order["product_price"])  + " ₽"
    bot.send_message(int(chat_id), message)


bot.polling(none_stop=True)