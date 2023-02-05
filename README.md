# Telegram bot to find a car

It'll help you to find a car at https://rapidapi.com/principalapis/api/car-data 
@EygenioBot - http://t.me/EygenioBot

You can run bot  with:

```bash
main.py
```

For development run:

```bash
SITE_API = Your key received from the API at 'https://rapidapi.com/principalapis/api/car-data'
HOST_API = X-RapidAPI-Host from the site: 'https://rapidapi.com/principalapis/api/car-data'
BOT_TOKEN = 'YOUR_TOKEN' yarn run develop
```

You can run bot check commands:

```bash
/start - to run the bot
/help - to show available commands
/history - to show ten last commands
/low - to show the oldest cars
/high - to show latest cars
/custom xxxx - xxxx - to show cars in your range
```