import requests
import json
import redis
REDIS_HOST = 'redis-10076.c1.asia-northeast1-1.gce.cloud.redislabs.com' #Адрес хоста Redis
REDIS_PORT = 10076 #номер порта в Redis
REDIS_PASSWORD = '' # Пароль в Redis
BOT_TOKEN = '' #Токен Телеграм-бота
WEBSITE_APIKEY = '' #API ключ вебсайта
WEBSITE = 'https://api.apilayer.com/exchangerates_data/convert?to=[to_curr]&from=[from_curr]&amount=[amount]' #URL веб-страницы
red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
if json.loads(red.get('CURRENCIES')):
    CURRENCIES = json.loads(red.get('CURRENCIES'))
else:
    CURRENCIES = dict(json.loads(requests.get('https://api.apilayer.com/exchangerates_data/symbols',
                    headers={"apikey": WEBSITE_APIKEY}).content)['symbols'])
