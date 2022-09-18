from settings import settings as s
from moduls import extensions as e
import telebot
from telegram_bot_pagination import InlineKeyboardPaginator
from telebot import types as t

bot = telebot.TeleBot(s.BOT_TOKEN)
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = f'Для начала работы введите команду боту \n' \
           f'в формате:\n' \
           f'<из какой валюты перевести> <в какую валюту перевести> <количество валюты>\n' \
           f'Например: USD RUB 1000\n' \
           f'Либо, наберите команду /values или /convert и выберите нужные валюты\n' \


    bot.reply_to(message, text)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio', 'photo'])
def handle_docs_audio(message: telebot.types.Message):
    bot.reply_to(message, f'Бот принимает только текстовые команды!')


@bot.message_handler(commands=['convert', 'values'])
def convert(message: telebot.types.Message):
    #data = []
    text = 'Выберите валюту из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=get_markup(mode='base'))



def base_handler(call):
    #print(f'def base_handler(message: telebot.types.Message) {call.data.split("#")[1].split()}')
    base = call.data.split('#')[1]
    text = 'Выберите валюту в которую конвертировать:'
    bot.send_message(call.message.chat.id, text, reply_markup=get_markup(mode='quote', data=base), parse_mode='Markdown')


def quote_handler(call):
    #print(f'def quote_handler(message: telebot.types.Message, base): {call.data.split("#")[1].split()}')
    quote, base = call.data.split('#')[1].split()
    data = f'{base} {quote}'
    text = 'Введите количество валюты для конвертации:'
    bot.send_message(call.message.chat.id, text, reply_markup=get_amount_markup(mode='amount', data=data), parse_mode='Markdown')


def amount_handler(call):
    #print(f'def amount_handler(message: telebot.types.Message, base, quote): {call.data.split("#")[1].split()}')
    amount, base, quote = call.data.split('#')[1].split()
    convert_handler(call.message, base, quote, amount)


def convert_handler(message: telebot.types.Message, base, quote, amount):
    try:
        text = e.Cryptoconverter.get_price(base, quote, amount)
    except e.APIException as exc:
        bot.reply_to(message, f'{exc}')
    else:
        bot.reply_to(message, f'На текущий момент {amount} {base} ({e.CURRENCIES[base]}) можно обменять на {text} {quote} ({e.CURRENCIES[quote]})')


# def get_markup(page=1, mode = '', data = ''):
#     print(f'def get_markup: {mode} {data}')
#     paginator = InlineKeyboardPaginator(
#         len(e.CURRENCIES) // 10 + 1,
#         current_page=page,
#         data_pattern=f'page#{{page}} {data}'
#     )
#     curr_items = list(map(list, e.CURRENCIES.items()))[(page-1)*10:(page-1)*10 + 10]
#
#     for i in range(0, len(curr_items), 2):
#         item1 = t.InlineKeyboardButton(f'{curr_items[i][0]}:\t{curr_items[i][1]}', callback_data=f'{mode}#{curr_items[i][0]} {data}')
#         item2 = t.InlineKeyboardButton(f'{curr_items[i+1][0]}:\t{curr_items[i+1][1]}', callback_data=f'{mode}#{curr_items[i+1][0]} {data}')
#         paginator.add_before(item1, item2)
#     return paginator.markup


def get_markup(mode = '', data = ''):
    #print(f'def get_markup: {mode} {data}')
    keyboard = t.InlineKeyboardMarkup()
    curr_items = list(map(list, s.CURRENCIES.items()))
    for i in range(0, len(curr_items), 2):
        item1 = t.InlineKeyboardButton(f'{curr_items[i][0]}:\t{curr_items[i][1]}', callback_data=f'{mode}#{curr_items[i][0]} {data}')
        item2 = t.InlineKeyboardButton(f'{curr_items[i+1][0]}:\t{curr_items[i+1][1]}', callback_data=f'{mode}#{curr_items[i+1][0]} {data}')
        keyboard.add(item1, item2)
    return keyboard


def get_amount_markup(mode = '', data = ''):
    keyboard = t.InlineKeyboardMarkup()
    for i in [10, 100, 1000]:
        item1 = t.InlineKeyboardButton(f'{i}', callback_data=f'{mode}#{i} {data}')
        item2 = t.InlineKeyboardButton(f'{i * 1000}', callback_data=f'{mode}#{i * 1000} {data}')
        keyboard.add(item1, item2)
    return keyboard


def start():
    bot.polling(none_stop=True)


@bot.callback_query_handler(func=lambda call: True)
def tes(call):
    #print(call.data)
    mode = call.data.split('#')[0]
    if mode == 'base':
        base_handler(call)
    elif mode == 'quote':
        quote_handler(call)
    elif mode == 'amount':
        amount_handler(call)
    elif mode == 'page':
        page = int((call.data.split('#')[1]).split()[0])
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            'Выберите валюту:',
            reply_markup=get_markup(page, mode=mode, data=call.data.split()[-1]),
            parse_mode='Markdown'
        )
    else:
        print(call.data)


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
