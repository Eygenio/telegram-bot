import telebot

from telegram_bot_pagination import InlineKeyboardPaginator
from settings import BotSettings
from database.common.models import History, db
from main import db_write, db_read
from site_API.core import headers, params, site_api, url

token = BotSettings()

bot = telebot.TeleBot(token.bot_token.get_secret_value())

car_lines = {}


@bot.message_handler(commands=["start"])
def start_hello_world(message):
    """
    Функция реагирующая на команду в телеграмм-боте /start,
    отправляющая сообщение "Привет ✌️. Вас приветствует @EygenioBot." в телеграмм.
    """
    bot.send_message(message.chat.id, "Привет ✌️. Вас приветствует @EygenioBot.\n"
                                      "С моими возможностями можно ознакомиться в /help")


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
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
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
    отправляющая список автомобилей с наименьшим
    годом выпуска в функцию get_sorted_cars_list.
    """
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    cars_low_year = site_api.get_cars_low_year()
    response = cars_low_year("GET", url, headers, params)
    get_sorted_cars_list(response, message)


@bot.message_handler(commands=["high"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /high,
    отправляющая список автомобилей с наибольшим
    годом выпуска в функцию get_sorted_cars_list.
    """
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    cars_high_year = site_api.get_cars_high_year()
    response = cars_high_year("GET", url, headers, params)
    get_sorted_cars_list(response, message)


@bot.message_handler(commands=["custom"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /custom,
    отправляющая список автомобилей в заданном промежутке
    года выпуска в функцию get_sorted_cars_list.
    Из текста сообщения извлекаются только цифры, если их 8,
    то формируется промежуток лет, где первые 4 - начало, последние
    4 - конец, при этом если значение начала больше, чем значение конца,
    то меняет значения местами, далее если количество цифр не равно 8,
     выводит сообщение: "Хммм...не совсем понимаю, что Вы хотите, почитайте /help"
    """
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    result = ''
    for symbol in message.text:
        if symbol.isdigit():
            result += symbol

    if len(result) == 8:
        first_year = int(result[0:4])
        second_year = int(result[4:8])
        if first_year > second_year:
            first_year, second_year = second_year, first_year

        cars_custom_year = site_api.get_cars_custom_year()
        response = cars_custom_year("GET", url, headers, params, first_year, second_year)

        if response:
            get_sorted_cars_list(response, message)
        else:
            bot.send_message(message.chat.id, "Автомобили по данным годам отсутствуют")
    else:
        bot.send_message(message.chat.id, "Хммм...не совсем понимаю, что Вы хотите, почитайте /help")


@bot.message_handler(commands=["make"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /make,
    отправляющая список автомобилей заданной марки
    в функцию get_sorted_cars_list.
    Из текста сообщения отделяется часть после команды "/make "
    и происходит поиск по совпадению, если марка не найдена выводит сообщение:
    "Марка не найдена или неверно введено название"
    """
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    cars_buy_make = site_api.get_cars_buy_make()
    response = cars_buy_make("GET", url, headers, {"make": message.text[6:]})
    if response:
        get_sorted_cars_list(response, message)

    else:
        bot.send_message(message.chat.id, "Марка не найдена или неверно введено название")


@bot.message_handler(commands=["model"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /model,
    отправляющая спискок автомобилей заданной модели
    в функцию get_sorted_cars_list.
    Из текста сообщения отделяется часть после команды "/model "
    и происходит поиск по совпадению, если модель не найдена выводит сообщение:
   "Модель не найдена или неверно введено название"
    """
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    cars_buy_model = site_api.get_cars_buy_model()
    response = cars_buy_model("GET", url, headers, {"model": message.text[7:]})
    if response:
        get_sorted_cars_list(response, message)

    else:
        bot.send_message(message.chat.id, "Модель не найдена или неверно введено название")


@bot.message_handler(commands=["history"])
def start_message(message):
    """
    Функция реагирующая на команду в телеграмм-боте /history,
    отправляющая сообщение с последними 10 запросами в телеграмм.
    """
    history = []
    db_write(db, History, [{"message": message.text, "id_user": message.from_user.id}])
    retrieved = db_read(db, History, History.message, History.id_user)
    for element in retrieved:
        if element.id_user == str(message.from_user.id):
            history.append(element.message)
    if len(history) >= 10:
        history_line = ''.join(f'{command}\n' for command in history[len(history) - 10:])
        bot.send_message(message.chat.id, history_line)
    else:
        history_line = ''.join(f'{command}\n' for command in history[len(history) - 10:])
        bot.send_message(message.chat.id, history_line)
        bot.send_message(message.chat.id, history_line)
    history.clear()


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


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'character')
def characters_page_callback(call):
    """
    Функция для обработки нажатия кнопок, при выведении
    большого списка автомобилей, более 20-ти.
    """
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_character_page(call.message, page)


def get_sorted_cars_list(cars, message):
    """
    Функция сортирующая список автомобилей по году выпуску, марке, модели,
    после сортировки если список более 20-ти автомобилей, то разбивает на строки
    по 20 автомобилей и добавляет их в словарь car_lines для дальнейшего его выведения в
    телеграммботе
    :param cars: список автомобилей
    :param message: сообщение полученное в телеграмме
    """
    global car_lines
    car_lines[message.from_user.id] = []
    car_line = ''
    sorted_cars = sorted(cars, key=lambda element: (element["year"], element["make"], element["model"]))
    if len(sorted_cars) // 20 > 1:
        count = 0
        for car in sorted_cars:
            if count < 20:
                car_line += ''.join(f'{car["make"]} - {car["model"]} - {car["year"]} - {car["type"]}\n')
                count += 1
            else:
                car_lines[message.from_user.id].append(car_line)
                car_line = ''
                count = 0
        car_lines[message.from_user.id].append(car_line)
    else:
        car_lines[message.from_user.id] = [''.join(f'{car["make"]} - '
                                                   f'{car["model"]} - '
                                                   f'{car["year"]} - '
                                                   f'{car["type"]}\n' for car in sorted_cars)]

    send_character_page(message)


def send_character_page(message, page=1):
    """
    Функция пагинации словаря car_lines в зависимости
    от id пользователя и выведение в телеграмм
    :param message: сообщение полученное в телеграмме
    :param page: номер страницы
    """
    paginator = InlineKeyboardPaginator(
        len(car_lines[message.chat.id]),
        current_page=page,
        data_pattern='character#{page}'
    )

    bot.send_message(
        message.chat.id,
        car_lines[message.chat.id][page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


bot.infinity_polling()
