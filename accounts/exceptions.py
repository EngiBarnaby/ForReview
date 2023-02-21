from rest_framework import exceptions


class InvalidUniqueToken(exceptions.APIException):
    default_detail = 'Невалидный уникальный токен'
    default_code = 400
    status_code = 400


class WrongLoginOrPassword(exceptions.APIException):
    default_detail = 'Неверный логин или пароль'
    default_code = 400
    status_code = 400
