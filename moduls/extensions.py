from settings import settings as s
import requests
import json
class ConversionException(Exception):
    pass


class NotDecimalException(ConversionException):
    def __str__(self):
        return f'Количество для обмена должно быть положительным числом!'


class WrongNumberArgumentsException(ConversionException):
    def __str__(self):
        return f'Количество аргументов должно быть равно 3!'


class WrongCurrencyException(ConversionException):
    def __str__(self):
        return f'Одной из введённой валют не существует в списке!'


class SimilarCurrenciesException(ConversionException):
    def __str__(self):
        return f'Вы пытаетесь перевести в ту же валюту!'


class Cryptoconverter():
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        print(quote, base, amount)
        if quote == base:
            raise SimilarCurrenciesException

        if quote not in s.CURRENCIES.keys() or base not in s.CURRENCIES.keys():
            raise WrongCurrencyException

        if not amount.isdecimal() or float(amount) < 0:
            raise NotDecimalException

        url = s.WEBSITE.replace('[to_curr]', quote).replace('[from_curr]', base).replace('[amount]', amount)
        html = requests.get(url, headers={"apikey": s.WEBSITE_APIKEY}).content

        if not json.loads(html)['success']:
            raise ConversionException
        else:
            text = json.loads(html)['result']

        return text