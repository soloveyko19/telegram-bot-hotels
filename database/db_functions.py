""" Модуль функций для работы с БД """


from .models import Hotel


def add_hotel(hotel_name: str, user_telegram_id: int, command: str) -> None:
    """
    Функция добавления запроса отеля в БД

    Args:
         hotel_name (str): название отеля
         user_telegram_id (int): Телеграм id пользователя
         command (str): команда с которой был найден отель
    """
    Hotel.create(
        hotel_name=hotel_name,
        user_id=user_telegram_id,
        command=command
    )


def get_hotels_history(user_telegram_id: int) -> list:
    """
    Функция получения истории отеля.

    Возвращает последние 10 запросов пользователя по отелям.

    Args:
        user_telegram_id (int): Телеграм id пользователя

    Returns:
        hotel_history (list): последние 10 запросов пользователя
    """
    hotels = Hotel.select().where(Hotel.user_id == user_telegram_id).order_by(Hotel.added_at.desc()).limit(10)
    hotels_history = list()
    for hotel in hotels:
        hotels_history.append((hotel.hotel_name, hotel.command))
    return hotels_history
