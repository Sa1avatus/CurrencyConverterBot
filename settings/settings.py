REDIS_HOST = 'redis-10076.c1.asia-northeast1-1.gce.cloud.redislabs.com' #Адрес хоста Redis
REDIS_PORT = 10076 #номер порта в Redis
REDIS_PASSWORD = '' # Пароль в Redis
BOT_TOKEN = '' #Токен Телеграм-бота
WEBSITE_APIKEY = '' #API ключ вебсайта
WEBSITE = 'https://api.apilayer.com/exchangerates_data/convert?to=[to_curr]&from=[from_curr]&amount=[amount]' #URL веб-страницы
#Если не успею исправить обработку страниц до проверки проекта, то список валют берётся отсюда.
CURRENCIES = {
'USD': 'United States Dollar',
'EUR': 'Euro',
'GBP': 'British Pound Sterling',
'CHF': 'Swiss Franc',
'AUD': 'Australian Dollar',
'BRL': 'Brazilian Real',
'BTC': 'Bitcoin',
'CNY': 'Chinese Yuan',
'HKD': 'Hong Kong Dollar',
'IDR': 'Indonesian Rupiah',
'INR': 'Indian Rupee',
'JPY': 'Japanese Yen',
'KRW': 'South Korean Won',
'KZT': 'Kazakhstani Tenge',
'LTL': 'Lithuanian Litas',
'LVL': 'Latvian Lats',
'MXN': 'Mexican Peso',
'RUB': 'Russian Ruble',
'THB': 'Thai Baht',
'VND': 'Vietnamese Dong',
}
EXCHANGE_DATA = {
    "base": "",
    "quote": "",
    "amount": ""
}
