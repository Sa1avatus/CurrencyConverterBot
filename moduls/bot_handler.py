from settings import settings as s
from moduls import extensions as e
import telebot
from telegram_bot_pagination import InlineKeyboardPaginator


bot = telebot.TeleBot(s.BOT_TOKEN)
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = f'Для начала работы введите команду боту \n' \
           f'в формате:\n' \
           f'<из какой валюты перевести> <в какую валюту перевести> <количество валюты>\n' \
           f'Например: USD RUB 1000\n' \
           f'Для просмотра списка валют, наберите команду /values'
    bot.reply_to(message, text)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio', 'photo'])
def handle_docs_audio(message: telebot.types.Message):
    bot.reply_to(message, f'Бот принимает только текстовые команды!')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    send_page(message)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if len(message.text.split()) != 3:
            raise e.WrongNumberArgumentsException
        base, quote, amount = message.text.upper().split()
        text = e.Cryptoconverter.get_price(base, quote, amount)
    except e.APIException as exc:
        bot.reply_to(message, f'{exc}')
    else:
        bot.reply_to(message, f'На текущий момент {amount} {base} ({s.CURRENCIES[base]}) можно обменять на {text} {quote} ({s.CURRENCIES[quote]})')


def start():
    bot.polling(none_stop=True)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='page')
def page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_page(call.message, page)


def send_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(s.CURRENCIES) // 10 + 1,
        current_page=page,
        data_pattern='page#{page}'
    )
    text = 'Доступные для конвертации валюты:'
    for k in list(map(list, s.CURRENCIES.items()))[(page-1)*10:(page-1)*10 + 10]:
        text += f'\n{k[0]:5}:\t{k[1]}'
    paginator.add_after(telebot.types.InlineKeyboardButton('Go back', callback_data='back'))
    bot.send_message(
            message.chat.id,
            text,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
