from settings import settings as s
import requests
import json
from telegram_bot_pagination import InlineKeyboardPaginator


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


class Cryptoconverter():
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise SimilarCurrenciesException

        if quote not in s.CURRENCIES.keys() or base not in s.CURRENCIES.keys():
            raise WrongCurrencyException

        if not amount.isdecimal() or float(amount) < 0:
            raise NotDecimalException

        url = s.WEBSITE.replace('[to_curr]', quote).replace('[from_curr]', base).replace('[amount]', amount)
        html = requests.get(url, headers={"apikey": s.WEBSITE_APIKEY}).content

        if not json.loads(html)['success']:
            raise APIException
        else:
            text = json.loads(html)['result']

        return text


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'

