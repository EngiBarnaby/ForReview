from rest_framework import exceptions


class InvalidFilterParameter(exceptions.APIException):
    status_code = 400
    default_code = 400
    default_detail = 'Invalid filter parameter'


class InvalidImage(exceptions.APIException):
    status_code = 400
    default_code = 400
    default_detail = 'Невалидная фотография'


class ActualSystemConfigNotFound(exceptions.APIException):
    status_code = 400
    default_code = 400
    default_detail = 'Не определена актуальная версия конфигурации'
