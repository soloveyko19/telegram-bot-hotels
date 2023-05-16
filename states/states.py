from telebot.handler_backends import StatesGroup, State


class LowStates(StatesGroup):
    """ Состояния для опроса пользователя в по команде /low """
    city = State()
    hotel = State()


class HighStates(StatesGroup):
    """ Состояния для опроса пользователя в по команде /high """
    city = State()
    hotel = State()


class CustomStates(StatesGroup):
    """ Состояния для опроса пользователя в по команде /custom """
    city = State()
    price_from = State()
    price_to = State()
    hotel = State()


class AllStates(StatesGroup):
    """ Состояния для вывода информации по отелю """
    get_info = State()

