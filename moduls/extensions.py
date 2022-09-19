from settings import settings as s
import requests
import json
from telegram_bot_pagination import InlineKeyboardPaginator
import redis


class APIException(Exception):
    pass


class NotDecimalException(APIException):
    def __str__(self):
        return f'Количество для обмена должно быть положительным числом!'


class WrongNumberArgumentsException(APIException):
    def __str__(self):
        return f'Количество аргументов должно быть равно 3!'


class WrongCurrencyException(APIException):
    def __str__(self):
        return f'Одной из введённой валют не существует в списке!'


class SimilarCurrenciesException(APIException):
    def __str__(self):
        return f'Вы пытаетесь перевести в ту же валюту!'


class NoConnectonException(APIException):
    def __str__(self):
        return f'Нет соединения с сервером API!'

# class TimeoutErrorException(APIException):
#     def __str__(self):
#         return f'Нет соединения с сервером API!'

class Cryptoconverter():
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise SimilarCurrenciesException

        if quote not in CURRENCIES.keys() or base not in CURRENCIES.keys():
            raise WrongCurrencyException

        if not str(amount).isdecimal() or float(str(amount)) < 0:
            raise NotDecimalException

        url = s.WEBSITE.replace('[to_curr]', quote).replace('[from_curr]', base).replace('[amount]', str(amount))
        html = requests.get(url, headers={"apikey": s.WEBSITE_APIKEY}).content

        if not json.loads(html)['success']:
            raise NoConnectonException
        else:
            text = json.loads(html)['result']

        return text


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


try:
    red = redis.Redis(host=s.REDIS_HOST, port=s.REDIS_PORT, password=s.REDIS_PASSWORD)
    CURRENCIES = json.loads(red.get('CURRENCIES'))
except Exception as e:
    print(f'Redis Error: {e}')
    try:
        CURRENCIES = dict(json.loads(requests.get('https://api.apilayer.com/exchangerates_data/symbols',
                                                  headers={"apikey": s.WEBSITE_APIKEY}).content)['symbols'])
    except Exception as e:
        print(f'WEBSITE Error: {e}')

