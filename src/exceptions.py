class NabronirivalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirivalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirivalException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExists(NabronirivalException):
    detail = "Уже существует "


class FoKeyObjectCannotBeDeleted(NabronirivalException):
    detail = "Оъект не может быть удален из за связанных данных в таблицах"
