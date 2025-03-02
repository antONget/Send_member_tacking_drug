from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_start_registration() -> InlineKeyboardMarkup:
    """
    Клавиатура для начала регистрации
    :return:
    """
    logging.info("keyboard_payment")
    button_1 = InlineKeyboardButton(text='Готовы продолжить?',
                                    callback_data='done_continue')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_select_marketplace() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора маркетплейса
    :return:
    """
    logging.info("keyboard_select_marketplace")
    button_1 = InlineKeyboardButton(text=f'Озон',
                                    callback_data=f'marketplace_ozon')
    button_2 = InlineKeyboardButton(text=f'Валдберрис',
                                    callback_data=f'marketplace_wildberries')
    button_3 = InlineKeyboardButton(text=f'ЯМаркет',
                                    callback_data=f'marketplace_yamarket')
    button_4 = InlineKeyboardButton(text=f'Сайт производителя',
                                    callback_data=f'marketplace_site')
    button_5 = InlineKeyboardButton(text=f'Другое',
                                    callback_data=f'marketplace_other')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5]])
    return keyboard



