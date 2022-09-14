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
    text = 'Доступные для конвертации валюты:'
    for k, v in s.CURRENCIES.items():
        text += f'\n{k:5}:\t{v}'
    #print(text)
    paginator = InlineKeyboardPaginator(
        len(s.CURRENCIES) // 10 + 1,
        current_page = 1,
        data_pattern = 'elements#{page}'
    )
    paginator.add_after(telebot.types.InlineKeyboardButton('Go back', callback_data='back'))
    bot.send_message(message.chat.id, text, reply_markup=paginator.markup, parse_mode='Markdown')
    #bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if len(message.text.split()) != 3:
            raise e.WrongNumberArgumentsException
        base, quote, amount = message.text.upper().split()
        text = e.Cryptoconverter.convert(base, quote, amount)
    except e.ConversionException as exc:
        bot.reply_to(message, f'{exc}')
    else:
        bot.reply_to(message, f'На текущий момент {amount} {base} можно обменять на {text} {quote}')


def start():
    bot.polling(none_stop=True)

