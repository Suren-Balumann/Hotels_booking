from fastapi import HTTPException, status


class NabronirivalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirivalException):
    detail = "Объект не найден"


class HotelNotFoundException(NabronirivalException):
    detail = "Отель не найден"


class RoomNotFoundException(NabronirivalException):
    detail = "Номер не найден"


class ObjectAlreadyExistsException(NabronirivalException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(NabronirivalException):
    detail = "Не осталось свободных номеров"


class FoKeyObjectCannotBeDeleted(NabronirivalException):
    detail = "Оъект не может быть удален из за связанных данных в таблицах"


class IncorrectTokenException(NabronirivalException):
    detail = "Не верный токен"


class ExpiredTokenException(NabronirivalException):
    detail = "Необхадимо авторизоваться"

class UserAlreadyExistsException(NabronirivalException):
    detail = "Пользователь уже существует"


class UserDoesNotRegisteredException(NabronirivalException):
    detail = "Пользователь не зарегестрирован"


class WrongPasswordException(NabronirivalException):
    detail = "Неверный пароль"

class NabronirovalHttpException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHttpException(NabronirovalHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отеля не существует"


class RoomNotFoundHttpException(NabronirovalHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Номера не существует"


class IncorrectTokenHttpException(NabronirovalHttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не верный токен"


class ExpiredTokenHttpException(NabronirovalHttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необхадимо авторизоваться"

class UserAlreadyExistsHttpException(NabronirovalHttpException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

class UserDoesNotRegisteredHttpException(NabronirovalHttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь с таким email не зарегестрирован"


class WrongPasswordHttpException(NabronirovalHttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль"

class AllRoomsAreBookedHttpException(NabronirovalHttpException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нет свободных номеров"