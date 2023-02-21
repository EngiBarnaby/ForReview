from rest_framework import exceptions


class UnknownError(exceptions.APIException):
    default_detail = 'Неизвестная ошибка'
    default_code = 400
    status_code = 400


class Interrupt(exceptions.APIException):
    default_detail = 'Поиск остановлен'
    default_code = 400
    status_code = 400


class InvalidUploadingData(exceptions.APIException):
    status_code = 400
    default_detail = 'Проверьте загружаемые данные на валидность'


class MultiEquipCategoryDownload(exceptions.APIException):
    status_code = 400
    default_detail = 'Можно выгружать только файлы данных номенклатур, относящихся к одной категории.'
