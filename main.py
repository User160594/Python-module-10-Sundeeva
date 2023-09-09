import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


TOKEN = '5764918310:AAGmQYl-Ge6HNVJ5gB-kg0hKEcDFB7keVU4'

bot = telebot.TeleBot(TOKEN)


exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты>\<имя валюты, в которую надо перевести>\
    <количество переводимой валюты>\nУвидеть список доступных валют можно, написав команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()







