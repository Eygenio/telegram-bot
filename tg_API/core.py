import telebot

from database.common.models import History, db
from main import db_write, db_read
from site_API.core import headers, params, site_api, url

token = "5972653478:AAEpTy0DN5K6fnvlO2Z09_omxSKWMkFrQl8"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["hello-world"])
def start_hello_world(message):
    """
    Функция реагирующая на команду в телеграмм-боте /hello-world,
    отправляющая сообщение "Привет ✌️. Вас приветствует @EygenioBot." в телеграмм.
    """
    bot.send_message(message.chat.id, "Привет ✌️. Вас приветствует @EygenioBot.")


@bot.message_handler(commands=["help"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /help,
    отправляющая сообщение со списком команд в телеграмм.
    """
    db_write(db, History, [{"message": message.text}])
    bot.send_message(message.chat.id, "Список команд:"
                                      "\n\t'/low' - выводит список автомобилей самого старого года выпуска;"
                                      "\n\t'/high' - выводит список автомобилей самого нового года выпуска;"
                                      "\n\t'/custom XXXX-XXXX' - выводит список автомобилей,"
                                      " заданного диапазона года выпуска;"
                                      "\n\t'/make XXXX' - выводит список автомобилей заданной марки"
                                      "\n\t'/model XXXX' - выводит список автомобилей заданной модели"
                                      "\n\t'/history' - выводит список последних 10-и запросов.")


@bot.message_handler(commands=["low"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /low,
    отправляющая сообщение со списком автомобилей с наименьшим
    годом выпуска, отсортированной по маркам и моделям, в телеграмм.
    """
    db_write(db, History, [{"message": message.text}])
    cars_low_year = site_api.get_cars_low_year()
    response = cars_low_year("GET", url, headers, params)
    sorted_response = sorted(response, key=lambda element: (element["make"], element["model"]))

    car_line = ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n' for car in sorted_response)
    if len(car_line) > 4096:
        for line in range(0, len(car_line), 4096):
            bot.send_message(message.chat.id, car_line[line:line + 4096])
    else:
        bot.send_message(message.chat.id, car_line)


@bot.message_handler(commands=["high"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /high,
    отправляющая сообщение со списком автомобилей с наибольшим
    годом выпуска, отсортированным по маркам и моделям, в телеграмм.
    """
    db_write(db, History, [{"message": message.text}])
    cars_high_year = site_api.get_cars_high_year()
    response = cars_high_year("GET", url, headers, params)
    sorted_response = sorted(response, key=lambda element: (element["make"], element["model"]))

    car_line = ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n' for car in sorted_response)
    if len(car_line) > 4096:
        for line in range (0, len(car_line), 4096):
            bot.send_message(message.chat.id, car_line[line:line + 4096])
    else:
        bot.send_message(message.chat.id, car_line)


@bot.message_handler(commands=["custom"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /custom,
    отправляющая сообщение со списком автомобилей в заданном
    промежутке года выпуска, отсортированным по годам, маркам и моделям, в телеграмм.
    Из текста сообщения извлекаются только цифры, если их 8,
    то формируется промежуток лет, где первые 4 - начало, последние
    4 - конец, если количество цифр не равно 8, выводит сообщение:
    "Хммм...не совсем понимаю, что Вы хотите, почитайте /help"
    """
    db_write(db, History, [{"message": message.text}])
    result = ''
    for symbol in message.text:
        if symbol.isdigit():
            result += symbol

    if len(result) == 8:
        first_year = int(result[0:4])
        second_year = int(result[4:8])

        cars_custom_year = site_api.get_cars_custom_year()
        response = cars_custom_year("GET", url, headers, params, first_year, second_year)
        sorted_response = sorted(response, key=lambda element: (element["year"], element["make"], element["model"]))

        car_line = ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n' for car in sorted_response)
        if len(car_line) > 4096:
            for line in range(0, len(car_line), 4096):
                bot.send_message(message.chat.id, car_line[line:line + 4096])
        else:
            bot.send_message(message.chat.id, car_line)
    else:
        bot.send_message(message.chat.id, "Хммм...не совсем понимаю, что Вы хотите, почитайте /help")


@bot.message_handler(commands=["make"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /make,
    отправляющая сообщение со списком автомобилей заданной
    марки, отсортированного по моделям, в телеграмм.
    Из текста сообщения отделяется часть после команды "/make "
    и происходит поиск по совпадению, если марка не найдена выводит сообщение:
    "Марка не найдена или неверно введено название"
    """
    db_write(db, History, [{"message": message.text}])
    cars_buy_make = site_api.get_cars_buy_make()
    response = cars_buy_make("GET", url, headers, {"make": message.text[6:]})
    if response:

        sorted_response = sorted(response, key=lambda element: (element["model"]))

        car_line = ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n' for car in sorted_response)
        if len(car_line) > 4096:
            for line in range(0, len(car_line), 4096):
                bot.send_message(message.chat.id, car_line[line:line + 4096])
        else:
            bot.send_message(message.chat.id, car_line)

    else:
        bot.send_message(message.chat.id, "Марка не найдена или неверно введено название")


@bot.message_handler(commands=["model"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /model,
    отправляющая сообщение со списком автомобилей заданной
    модели, отсортированного по маркам, в телеграмм.
    Из текста сообщения отделяется часть после команды "/model "
    и происходит поиск по совпадению, если модель не найдена выводит сообщение:
   "Модель не найдена или неверно введено название"
    """
    db_write(db, History, [{"message": message.text}])
    cars_buy_model = site_api.get_cars_buy_model()
    response = cars_buy_model("GET", url, headers, {"model": message.text[7:]})
    if response:

        sorted_response = sorted(response, key=lambda element: (element["make"]))

        car_line = ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n' for car in sorted_response)
        if len(car_line) > 4096:
            for line in range(0, len(car_line), 4096):
                bot.send_message(message.chat.id, car_line[line:line + 4096])
        else:
            bot.send_message(message.chat.id, car_line)

    else:
        bot.send_message(message.chat.id, "Модель не найдена или неверно введено название")


@bot.message_handler(commands=["history"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /history,
    отправляющая сообщение с последними 10 запросами в телеграмм.
    """
    db_write(db, History, [{"message": message.text}])
    retrieved = db_read(db, History, History.message)
    if len(retrieved) >= 10:
        history_line = ''.join(f'{element.message}\n' for element in retrieved[len(retrieved) - 10:])
        bot.send_message(message.chat.id, history_line)
    else:
        history_line = ''.join(f'{element.message}\n' for element in retrieved)
        bot.send_message(message.chat.id, history_line)


@bot.message_handler(content_types=['text'])
def start_hello(message):
    """
    Функция реагирующая на введенный текст, если введено сообщение "привет",
    любого регистра, выводит сообщение "Привет ✌️. Вас приветствует @EygenioBot. ",
    в противном случае выводит сообщение "Хммм...не совсем понимаю, что Вы хотите, почитайте /help".
    """
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет ✌️. Вас приветствует @EygenioBot. ")
    else:
        bot.send_message(message.chat.id, "Хммм...не совсем понимаю, что Вы хотите, почитайте /help")


bot.infinity_polling()
