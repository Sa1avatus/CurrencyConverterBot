from settings import settings as s
from moduls import extensions as e
import telebot
from telegram_bot_pagination import InlineKeyboardPaginator
from telebot import types as t
import json
import ast

bot = telebot.TeleBot(s.BOT_TOKEN)
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = f'''Для начала работы введите команду боту
в формате:
<из какой валюты перевести> <в какую валюту перевести> <количество валюты>
Например: USD RUB 1000
Либо, наберите команду /values или /convert и выберите нужные валюты'''
    bot.reply_to(message, text)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio', 'photo'])
def handle_docs_audio(message: telebot.types.Message):
    bot.reply_to(message, f'Бот принимает только текстовые команды!')


@bot.message_handler(commands=['convert', 'values'])
def convert(message: telebot.types.Message):
    data = s.EXCHANGE_DATA.copy()
    data['m'] = 'b'
    text = 'Выберите валюту из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=get_markup(data))



def base_handler(call):
    #print(f'def base_handler(message: telebot.types.Message) {call.data}')
    #print(type(call.data.split('#')[1]))
    data = data_normalisation(call.data.split('#')[-1])
    data['m'] = 'q'
    text = 'Выберите валюту в которую конвертировать:'
    bot.send_message(call.message.chat.id, text, reply_markup=get_markup(data), parse_mode='Markdown')


def quote_handler(call):
    #print(f'def quote_handler(message: telebot.types.Message, base): {call.data}')
    data = data_normalisation(call.data.split('#')[-1])
    data['m'] = 'am'
    text = 'Введите количество валюты для конвертации:'
    bot.send_message(call.message.chat.id, text, reply_markup=get_amount_markup(data), parse_mode='Markdown')


def amount_handler(call):
    #print(f'def amount_handler(message: telebot.types.Message, base, quote): {call.data}')
    data = data_normalisation(call.data.split('#')[-1])
    convert_handler(call.message, **data)


def convert_handler(message: telebot.types.Message, m, b, q, am):
    try:
        text = e.Cryptoconverter.get_price(b, q, am)
    except e.APIException as exc:
        bot.reply_to(message, f'{exc}')
    else:
        bot.reply_to(message, f'На текущий момент {am} {b} ({e.CURRENCIES[b]}) можно обменять на {text} {q} ({e.CURRENCIES[q]})')


def get_markup(data, page=1):
    #print(f'def get_markup: {data} {type(data)}')
    data = data_normalisation(data)
    mode = data['m']
    paginator = InlineKeyboardPaginator(
        len(e.CURRENCIES) // 10 + 1,
        current_page=page,
        data_pattern=f'page#{{page}}#{str(data).replace("{", "(").replace("}", ")")}'
    )
    curr_items = list(map(list, e.CURRENCIES.items()))[(page-1)*10:(page-1)*10 + 10]

    for i in range(0, len(curr_items), 2):
        dt1 = data.copy()
        dt2 = data.copy()
        dt1[mode] = curr_items[i][0]
        dt2[mode] = curr_items[i+1][0]
        item1 = t.InlineKeyboardButton(f'{curr_items[i][0]}:\t{curr_items[i][1]}', callback_data=f'{mode}#{dt1}')
        item2 = t.InlineKeyboardButton(f'{curr_items[i+1][0]}:\t{curr_items[i+1][1]}', callback_data=f'{mode}#{dt2}')
        paginator.add_before(item1, item2)
    return paginator.markup


def get_amount_markup(data):
    keyboard = t.InlineKeyboardMarkup()
    data = data_normalisation(data)
    mode = data['m']
    for i in [10, 100, 1000]:
        dt1 = data.copy()
        dt2 = data.copy()
        dt1['am'] = i
        dt2['am'] = i * 1000
        item1 = t.InlineKeyboardButton(f'{i}', callback_data=f'{mode}#{dt1}')
        item2 = t.InlineKeyboardButton(f'{i * 1000}', callback_data=f'{mode}#{dt2}')
        keyboard.add(item1, item2)
    return keyboard


def data_normalisation(data):
    data = str(data).replace("(", "{").replace(")", "}")
    data = ast.literal_eval(data)
    return data


def start():
    bot.polling(none_stop=True)


@bot.callback_query_handler(func=lambda call: True)
def tes(call):
    #print(f'def tes(call): {call.data}')
    data = data_normalisation(call.data.split('#')[-1])
    mode = data['m']
    if call.data.split('#')[0] == 'page':
        page = int(call.data.split('#')[1])
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            'Выберите валюту:',
            reply_markup=get_markup(call.data.split('#')[-1], page),
            parse_mode='Markdown'
        )
    elif mode == 'b':
        base_handler(call)
    elif mode == 'q':
        quote_handler(call)
    elif mode == 'am':
        amount_handler(call)
    elif mode == 'page':
        page = int(call.data.split('#')[1])
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            'Выберите валюту:',
            reply_markup=get_markup(call.data.split('#')[-1], page),
            parse_mode='Markdown'
        )
    else:
        pass
        #print(call.data)


@bot.message_handler(content_types=['text'])
def convert_text(message: telebot.types.Message):
    try:
        if len(message.text.split()) != 3:
            raise e.WrongNumberArgumentsException
        base, quote, amount = message.text.upper().split()
        text = e.Cryptoconverter.get_price(base, quote, amount)
    except e.APIException as exc:
        bot.reply_to(message, f'{exc}')
    else:
        bot.reply_to(message, f'На текущий момент {amount} {base} ({e.CURRENCIES[base]}) можно обменять на {text} {quote} ({e.CURRENCIES[quote]})')


