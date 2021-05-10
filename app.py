import telebot
from config import keys, token
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def help1(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<колличество переводимой валюты> \n ' \
           'Чтобы увидить список всех доступных валют введите команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values1(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert1(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не верное количество параметров')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')

    else:
        text = f'Стоимость {amount} {base} равна {total_base} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()