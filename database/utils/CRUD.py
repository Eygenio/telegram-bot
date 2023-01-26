from typing import Dict, List, TypeVar
from peewee import ModelSelect
from database.common.models import ModelBase
from ..common.models import db

T = TypeVar("T")


def _store_date(db: db, model: T, *date: List[Dict]) -> None:
    """
    Функция, добавления записи в базу данных
    :param db: база данных
    :param model: модель
    :param date: данные
    """
    with db.atomic():
        model.insert_many(*date).execute()


def _retrieve_all_data(db: db, model: T, *columns: ModelBase) -> ModelSelect:
    """
    Функция, получения записи из базы данных
    :param db: база данных
    :param model: модель
    :return: возвращает данные из базы данных
    """
    with db.atomic():
        response = model.select(*columns)

    return response


class CRUDInteface():
    """
    Базовый класс обращения к базе данных.
    """
    @staticmethod
    def create():
        """
        Метод обращения к функции _store_date
        """
        return _store_date

    @staticmethod
    def retrieve():
        """
        Метод обращения к функции _retrieve_all_data
        """
        return _retrieve_all_data


if __name__ == "__main__":
    _store_date()
    _retrieve_all_data()
    CRUDInteface()
