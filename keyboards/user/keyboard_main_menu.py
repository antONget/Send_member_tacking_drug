from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_start_menu() -> InlineKeyboardMarkup:
    """
    Клавиатура изменения или подтверждения даты
    :return:
    """
    logging.info("keyboard_payment")
    button_1 = InlineKeyboardButton(text='Баланс',
                                    callback_data='main_menu_balance')
    button_2 = InlineKeyboardButton(text='Время приема коллагена',
                                    callback_data='main_menu_time')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_change_time() -> InlineKeyboardMarkup:
    """
    Клавиатура изменения или подтверждения даты
    :return:
    """
    logging.info("keyboard_payment")
    button_1 = InlineKeyboardButton(text='Изменить время',
                                    callback_data='change_time')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard
