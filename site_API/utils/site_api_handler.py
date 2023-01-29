from typing import Dict, Any, List
from time import sleep

import requests


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int = 10) -> Any:
    """
    Функция формирующая запрос на API, возвращая полученный ответ.
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :return: возвращается ответ от запроса на API.
    """
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
        if response.status_code == requests.codes.ok:
            return response

    except Exception:
        print('Ошибка, нет ответа от сервера.')


def _get_cars_low_year(method: str, url: str, headers: Dict, params: Dict, func=_make_response) -> List:
    """
    Функция, которая формирует список автомобилей с наименьшим годом выпуска
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :param func: функция для запроса на API
    :return: возвращается список автомобилей с наименьшим годом выпуска
    """
    response = []

    url_year = "{0}/cars/years".format(url)
    year = min(func(method, url_year, headers=headers, params=params).json())
    sleep(1)

    params = {"limit": 50, "page": 0, "year": year}
    url = "{0}/cars".format(url)
    result = func(method, url, headers=headers, params=params)
    sleep(1)

    while result.json():
        for car in result.json():
            response.append(car)

        params["page"] += 1
        result = func(method, url, headers=headers, params=params)
        sleep(1)
        result.json()

        for car in result.json():
            response.append(car)

    return response


def _get_cars_high_year(method: str, url: str, headers: Dict, params: Dict, func=_make_response) -> List:
    """
    Функция, которая формирует список автомобилей с наибольшим годом выпуска
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :param func: функция для запроса на API
    :return: возвращается список автомобилей с наибольшим годом выпуска
    """
    response = []

    url_year = "{0}/cars/years".format(url)
    year = max(func(method, url_year, headers=headers, params=params).json())
    sleep(1)

    params = {"limit": 50, "page": 0, "year": year}
    url = "{0}/cars".format(url)
    result = func(method, url, headers=headers, params=params)
    sleep(1)

    while result.json():
        for car in result.json():
            response.append(car)

        params["page"] += 1
        result = func(method, url, headers=headers, params=params)
        sleep(1)
        result.json()

        for car in result.json():
            response.append(car)

    return response


def _get_cars_custom_year(method: str, url: str, headers: Dict, params: Dict,
                          start_year: int, finish_year: int, func=_make_response) -> List:
    """
    Функция, которая формирует список автомобилей с годом выпуска диапазона от start_year до finish_year
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :param start_year: начало диапазона формирования списка
    :param start_year: конец диапазона формирования списка
    :param func: функция для запроса на API
    :return: возвращается список автомобилей с наибольшим годом выпуска
    """
    response = []
    years_list = []
    url_year = "{0}/cars/years".format(url)
    years = func(method, url_year, headers=headers, params=params).json()
    sleep(1)

    for year in range(start_year, finish_year + 1):
        if year in years:
            years_list.append(year)

    url = "{0}/cars".format(url)

    for get_year in years_list:
        params = {"limit": 50, "page": 0, "year": get_year}
        result = func(method, url, headers=headers, params=params)
        sleep(1)

        for car in result.json():
            response.append(car)

        while result.json():

            params["page"] += 1
            result = func(method, url, headers=headers, params=params)
            sleep(1)
            result.json()

            for car in result.json():
                response.append(car)

    return response


def _get_cars_buy_make(method: str, url: str, headers: Dict, params: Dict, func=_make_response) -> List:
    """
    Функция, которая формирует список автомобилей заданной марки
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :param func: функция для запроса на API
    :return: возвращается список автомобилей заданной марки
    """
    response = []

    url = "{0}/cars".format(url)
    result = func(method, url, headers=headers, params=params)
    result.json()

    for car in result.json():
        response.append(car)

    return response


def _get_cars_buy_model(method: str, url: str, headers: Dict, params: Dict, func=_make_response) -> List:
    """
    Функция, которая формирует список автомобилей заданной модели
    :param method: строка для формирования запроса на API
    :param url: ссылка API
    :param headers: пользовательские данные доступа к API
    :param params: параметры запроса на API
    :param func: функция для запроса на API
    :return: возвращается список автомобилей заданной модели
    """
    response = []

    url = "{0}/cars".format(url)
    result = func(method, url, headers=headers, params=params)
    result.json()

    for car in result.json():
        response.append(car)

    return response


class SiteApiInterface():
    """
    Базовый класс запросов к API.
    """

    @staticmethod
    def get_cars_low_year():
        """
        Метод обращения к функции _get_cars_low_year
        """
        return _get_cars_low_year

    @staticmethod
    def get_cars_high_year():
        """
        Метод обращения к функции _get_cars_high_year
        """
        return _get_cars_high_year

    @staticmethod
    def get_cars_custom_year():
        """
        Метод обращения к функции _get_cars_custom_year
        """
        return _get_cars_custom_year

    @staticmethod
    def get_cars_buy_make():
        """
        Метод обращения к функции _get_cars_buy_make
        """
        return _get_cars_buy_make

    @staticmethod
    def get_cars_buy_model():
        """
        Метод обращения к функции _get_cars_buy_model
        """
        return _get_cars_buy_model


if __name__ == "__main__":
    _make_response()
    _get_cars_low_year()
    _get_cars_high_year()
    _get_cars_custom_year()
    _get_cars_buy_make()
    _get_cars_buy_model()

    SiteApiInterface()
