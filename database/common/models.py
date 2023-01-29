from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('lecture.db')


class ModelBase(pw.Model):
    """
    Класс Базовая Модель. Родитель: pw.Model
    created_at: поле, даты когда был сделан запрос
    """
    created_at = pw.DateTimeField(default=datetime.now)

    class Meta():
        """
        Класс Мета
        database: указывает, что таблица истории принадлежит базе данных
        """

        database = db


class History(ModelBase):
    """
    Класс История. Родитель:ModelBase
    message: поле, теста запроса сохраненного в истории
    """
    message = pw.TextField()
