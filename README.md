# CurrencyExchangeBot
Телеграмм бот по курсам валют.

API-ключи необходимо внести в файл ./settings/settings.py

#### Зависимости

    pip3 install pyTelegramBotAPI
    pip3 install lxml
    pip3 install requests
    pip3 install redis
    pip3 install json
    pip3 install python-telegram-bot-pagination #https://github.com/ksinn/python-telegram-bot-pagination
    

#### Запуск
    
    py .\start.py

#### Команды

    Бот принимает команды:
    /start, /help - показывает доступные команды и инструкциюпо применению
    /values - показывает доступные валюты для конвертации
    
#### Формат сообщений
    <из какой валюты перевести> <в какую валюту перевести> <количество валюты>
    
#### Пример
    USD RUB 1000
