from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_select_drug() -> InlineKeyboardMarkup:
    """
    Клавиатура для препарата
    :return:
    """
    logging.info("keyboard_select_marketplace")
    button_1 = InlineKeyboardButton(text=f'со вкусом лимона - 15 саше',
                                    callback_data=f'type_drug_limon_15')
    button_2 = InlineKeyboardButton(text=f'со вкусом апельсина - 15 саше',
                                    callback_data=f'type_drug_orange_15')
    button_3 = InlineKeyboardButton(text=f'со вкусом грейпфрута - 15 саше',
                                    callback_data=f'type_drug_grapefruit_15')
    button_4 = InlineKeyboardButton(text=f'со вкусом лимона - 30 саше',
                                    callback_data=f'type_drug_limon_30')
    button_5 = InlineKeyboardButton(text=f'со вкусом апельсина - 30 саше',
                                    callback_data=f'type_drug_orange_30')
    button_6 = InlineKeyboardButton(text=f'со вкусом грейпфрута - 30 саше',
                                    callback_data=f'type_drug_grapefruit_30')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1],
                                                     [button_2],
                                                     [button_3],
                                                     [button_4],
                                                     [button_5],
                                                     [button_6]])
    return keyboard


def keyboard_start_registration() -> InlineKeyboardMarkup:
    """
    Клавиатура изменения или подтверждения даты
    :return:
    """
    logging.info("keyboard_payment")
    button_1 = InlineKeyboardButton(text='Изменить дату',
                                    callback_data='date_start_change')
    button_2 = InlineKeyboardButton(text='Продолжить',
                                    callback_data='date_start_confirm')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard
